"""Implements the "Bottle" interface."""
import io
import json
import uuid
from typing import Dict, List, Any, Tuple, Union

import requests

from ialib.genome_info import Genome


class QueryError(Exception):
    """Raised if any query to any node returns an error."""
    pass


class ConnectionError(Exception):
    """Raised if any query to any node returns an error."""
    pass


def remove_unique_id(response: dict) -> dict:
    """Return *response* with the key 'unique_id' removed regardless of nesting."""
    if isinstance(response, dict):
        if 'unique_id' in response:
            del (response['unique_id'])
        for value in response.values():
            if isinstance(value, dict):
                remove_unique_id(value)
    return response


class BottleClient:
    """Interface for interacting with bottles."""

    def __init__(self, bottle_info):
        """
        Provide bottle information in a dictionary.

        ex:
        from ialib.BottleClient import BottleClient

        bottle_info = {'api_key': 'ABCD-1234',
                    'name': 'genie-bottle',
                    'domain': 'intelligent-artifacts.com',
                    'secure': False}

        bottle = BottleClient(bottle_info)
        bottle.connect()

        bottle.setIngressNodes(['P1'])
        bottle.setQueryNodes(['P1'])

        """
        self.genome = None
        self.bottle_info = bottle_info
        self.name = bottle_info['name']
        self.domain = bottle_info['domain']
        self.api_key = bottle_info['api_key']
        self.ingress_nodes = []
        self.query_nodes = []
        self.headers = {'X-API-KEY': self.api_key}
        self.all_nodes = []
        self.failures = []
        self._connected = False
        self.genome = None
        self.genie = None
        self.send_unique_ids = True
        self.summarize_for_single_node = True
        if 'secure' not in self.bottle_info or self.bottle_info['secure']:
            self.secure = True
            self.url = 'https://{name}.{domain}/'.format(**self.bottle_info)
        else:
            self.secure = False
            self.url = 'http://{name}.{domain}/'.format(**self.bottle_info)

    def __repr__(self) -> str:
        return '<{name}.{domain}| secure: %r, connected: %s, genie: %s, \
                  ingress_nodes: %i, query_nodes: %i, failures: %i>'.format(
            **self.bottle_info) % (
                   self.secure, self._connected, self.genie, len(self.ingress_nodes), len(self.query_nodes),
                   len(self.failures))

    def receive_unique_ids(self, should_set: bool = True) -> bool:
        self.send_unique_ids = should_set
        return self.send_unique_ids

    def connect(self) -> Dict:
        """Grabs the bottle's genie's genome for node definitions."""
        response_data = requests.get(self.url + 'connect', verify=self.secure, headers=self.headers).json()
        if 'status' not in response_data or response_data['status'] != 'okay':
            self._connected = False
            raise ConnectionError("Connection failed!", response_data)

        self.genome = Genome(response_data['genome'])
        self.genie = response_data['genome']['agent']
        self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        if response_data['connection'] == 'okay':
            self._connected = True
        else:
            self._connected = False

        return {'connection': response_data['connection'], 'genie': response_data['genie']}

    def set_ingress_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define where data will be sent."""
        if nodes is None:
            nodes = []
        self.ingress_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.ingress_nodes

    def set_query_nodes(self, nodes: List = None) -> List:
        """Use list of primitive names to define which nodes should return answers."""
        if nodes is None:
            nodes = []
        self.query_nodes = [{'id': self.genome.primitive_map[node], 'name': node} for node in nodes]
        return self.query_nodes

    def _query(self, query_method: Any, path: str, data: Dict = None, nodes: List = None,
               unique_id: str = None) -> Union[dict, Tuple[dict, str]]:
        """Internal helper function to make an RPC call with the given *query* and *data*."""
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        result = {}
        if unique_id is not None:
            if data:
                data['unique_id'] = unique_id
            else:
                data = {'unique_id': unique_id}

        if isinstance(nodes[0], str):
            nodes = [{'name': name, 'id': self.genome.primitive_map[name]} for name in nodes]
        for node in nodes:
            full_path = f'{self.url}{node["id"]}/{path}'
            try:
                if data is not None:
                    response = query_method(full_path, verify=self.secure, headers=self.headers,
                                            json={'data': data})
                else:
                    response = query_method(full_path, verify=self.secure, headers=self.headers)
                response.raise_for_status()
                response = response.json()
                if response['status'] != 'okay':
                    self.failures.append({node['name']: {'message': response['messsage']}})
                if not self.send_unique_ids:
                    response = remove_unique_id(response['message'])
                else:
                    response = response['message']
                if len(nodes) == 1 and self.summarize_for_single_node:
                    result = response
                else:
                    result[node['name']] = response
            except Exception as exception:
                self.failures.append({node['name']: {'class': exception.__class__.__name__, 'message': str(exception)}})
                raise QueryError("Query Failure:",
                                 {'class': exception.__class__.__name__, 'message': str(exception)}) from exception
        if unique_id is not None:
            return result, unique_id
        return result

    def set_summarize_for_single_node(self, value: bool):
        self.summarize_for_single_node = value

    def observe(self, data: Dict, nodes: List = None) -> Union[dict, Tuple[dict, str]]:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'observe', data=data, nodes=nodes)

    def observe_event(self, data: Dict, unique_id: str = None) -> Tuple[dict, str]:
        """Exclusively uses the 'observe' call.  All commands must be provided via Genie Metalanguage data."""
        results = {}
        uid = None
        if unique_id is None:
            unique_id = str(uuid.uuid4())
        for node, node_data in data.items():
            response, uid = self._query(requests.post, 'observe', data=node_data, nodes=[node], unique_id=unique_id)
            results[node] = response
        return results, uid

    def observe_classification(self, data=None, nodes: List = None):
        """
        Best practice is to send a classification to all [ingress and] query nodes as a singular symbol in the last event.
        This function does that for us.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.query_nodes
        return self._query("observe", data, nodes=nodes)

    def show_status(self, nodes: List = None) -> List:
        """Return the current status of the bottle."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'status', nodes=nodes)

    def learn(self, nodes: List = None) -> List:
        """Return the learn results."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'learn', nodes=nodes)

    def get_wm(self, nodes: List = None) -> List:
        """Return information about Working Memory."""
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'working-memory', nodes=nodes)

    def get_predictions(self, unique_id: str = None, nodes: List = None) -> List:
        """Return prediction result data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'predictions', nodes=nodes, unique_id=unique_id)

    def get_hive_prediction_utility(self) -> dict:
        """Return prediction result data."""
        return requests.post(
            f'{self.url}predictions/utility',
            headers=self.headers,
            json={'data': {'primitive_ids': [primitive['id'] for primitive in self.query_nodes]}}).json()

    def clear_wm(self, nodes: List = None) -> List:
        """Clear the Working Memory of the Genie."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'working-memory/clear', nodes=nodes)

    def clear_all_memory(self, nodes: List = None) -> List:
        """Clear both the Working Memory and persisted memory."""
        if nodes is None:
            nodes = self.ingress_nodes
        return self._query(requests.post, 'clear-all-memory', nodes=nodes)

    def get_percept_data(self, nodes: List = None) -> List:
        """Return percept data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'percept-data', nodes=nodes)

    def get_cognition_data(self, nodes: List = None) -> List:
        """Return cognition data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'cognition-data', nodes=nodes)

    def get_decision_table(self, nodes: List = None) -> List:
        """Return a decision table."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'decision-table', nodes=nodes)

    def get_action_data(self, nodes: List = None) -> List:
        """Return action data."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.get, 'action-data', nodes=nodes)

    def change_genes(self, gene_data: Dict, nodes: List = None) -> List:
        """
        Use primitive names.
        This will do live updates to an existing agent, rather than stopping an agent and starting a new one as per 'injectGenome'.
        gene_data of form:

            {gene: value}

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]

        result = {}
        for node in nodes:  ## only primitive nodes at this time.
            response = requests.post(f"{self.url}{node['id']}/genes/change",
                                     verify=self.secure, headers=self.headers,
                                     json={'data': gene_data}).json()
            if 'error' in response or response['status'] == 'failed':
                if len(nodes) == 1 and self.summarize_for_single_node:
                    raise Exception("Request Failure:", response)
                self.failures.append({node['name']: response})
                print("Failure:", {node['name']: response})
            self.genome.change_genes(node['id'], gene_data)
            if len(nodes) == 1 and self.summarize_for_single_node:
                return response['message']
            result[node['name']] = response['message']
        return result

    def inject_genome(self, genome: Dict) -> Dict:
        """Halt all primitives in the current bottle and start those described in *genome*.

        *genome* must be either a JSON-serializable object or a file-like object.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if isinstance(genome, io.TextIOBase):
            genome = json.load(genome)
        response = requests.post(f'{self.url}genome/inject', verify=self.secure, headers=self.headers,
                                 json={'genome': genome}).json()
        if 'error' not in response:
            self.genome = Genome(genome)
            self.genie = self.genome.agent
            self.all_nodes = [{"name": i['name'], "id": i['id']} for i in self.genome.primitives.values()]
        return response

    def get_cost_benefit(self, nodes: List = None) -> List:
        """Return cost benefit"""
        if nodes is None:
            nodes = self.query_nodes
        return self._query('getCostBenefit', nodes=nodes)

    def get_gene(self, gene: str, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Use primitive names.
        This will return the gene value of an existing agent, gene_data of form (similar to that
        of the change_genes method):

            gene

        where gene is the name of the gene.

        Only works on primitive nodes at this time.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.get(f"{self.url}{node['id']}/gene/{gene}",
                                        verify=self.secure,
                                        headers=self.headers).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    self.failures.append({node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {gene: response['message']}
                result[node['name']] = {gene: response['message']}
            except Exception as exception:
                self.failures.append({node['name']: exception})
                raise Exception("Request Failure:", {node['name']: exception})

        return result

    def get_model(self, model_name: Dict, nodes: List = None) -> List[Dict[str, Dict[str, str]]]:
        """
        Returns model.

        data : {primitive_name : name}

        Model name is unique, so it should not matter that we query all nodes, only
        one model will be found. How will the absense of a name in a primitive be
        conveyed?
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.get(f"{self.url}{node['id']}/model/{model_name}",
                                        headers=self.headers,
                                        verify=self.secure).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    self.failures.append({node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                else:
                    result[node['name']] = response['message']
            except Exception as exception:
                self.failures.append({node['name']: exception})
                raise Exception("Request Failure:", {node['name']: exception})

        return result

    def get_name(self, nodes: List = None) -> List[Dict[str, str]]:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'name', nodes=nodes)

    def get_time(self, nodes: List = None) -> List:
        """
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.get, 'time', nodes=nodes)

    def get_vector(self, vector_name: str, nodes: List = None) -> List:
        """
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.post(self.url, verify=self.secure, json={"method": "getVector",
                                                                             "params": {"api_key": self.api_key,
                                                                                        "primitive_id": node['id'],
                                                                                        "data": vector_name},
                                                                             "jsonrpc": "2.0", "id": 1}).json()[
                    'result']
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    self.failures.append({node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {vector_name: response}
                result[node['name']] = {vector_name: response}
            except Exception as exception:
                self.failures.append({node['name']: exception})
                raise
        return result

    def increment_recall_threshold(self, increment: float, nodes: List = None) -> List[Dict[str, Any]]:
        """
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            nodes = self.all_nodes
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        result = {}
        for node in nodes:
            try:
                response = requests.post(f"{self.url}{node['id']}/gene/increment-recall-threshold",
                                         verify=self.secure, headers=self.headers,
                                         json={'increment': increment}).json()
                if 'error' in response or response['status'] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    self.failures.append({node['name']: response})
                else:
                    self.genome.primitives[node['id']]['recall_threshold'] += increment
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return {"recall_threshold": response['message']}
                result[node['name']] = {"recall_threshold": response['message']}
            except Exception as exception:
                self.failures.append({node['name']: exception})
                raise

        return result

    def show_predictions_knowledge_details(self) -> List:
        """
        """
        return []

    def start_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Allow query nodes to start acting.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/start', nodes=nodes)

    def stop_acting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Stop query nodes from acting.
        """
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'acting/stop', nodes=nodes)

    def start_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Tells all nodes to start sleeping.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/start', nodes=nodes)

    def stop_sleeping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Wakes up all sleeping nodes.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'sleeping/stop', nodes=nodes)

    def start_predicting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Tells all nodes to start predicting.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'predicting/start', nodes=nodes)

    def stop_predicting(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Tells all nodes to stop predicting. Useful for faster training, but abstracted nodes will not learn.
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'predicting/stop', nodes=nodes)

    def ping(self, nodes: List = None) -> List[Dict[str, Any]]:
        """Ping a node to ensure it's up."""
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        if nodes is None:
            return requests.get(f'{self.url}bottle/ping', headers=self.headers).json()
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
            results = {}
            for node in nodes:
                response = requests.get(f"{self.url}{node['id']}/ping", verify=self.secure,
                                        headers=self.headers).json()
                if 'error' in response or response["status"] == 'failed':
                    if len(nodes) == 1 and self.summarize_for_single_node:
                        raise Exception("Request Failure:", response)
                    print("Failure:", {node['name']: response})
                if len(nodes) == 1 and self.summarize_for_single_node:
                    return response['message']
                results[node['name']] = response["message"]
            return results

    def define_mood(self, mood_list: List, nodes: List = None) -> List:
        """
        *mood_data* should be of the format:
            [emotive-1, emotive-2]

        where node-name is the *name* of a primitive or manipulative.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        results = {}
        if nodes is None:
            nodes = [node['name'] for node in self.all_nodes]
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        for node in nodes:
            response = requests.post(f"{self.url}{node['id']}/mood/define", verify=self.secure,
                                     headers=self.headers, json={'data': mood_list}).json()
            if 'error' in response or response['status'] == 'failed':
                if len(nodes) == 1 and self.summarize_for_single_node:
                    raise Exception("Request Failure:", response)
                self.failures.append({node['name']: response})
                print("Failure:", {node['name']: response})
            if len(nodes) == 1 and self.summarize_for_single_node:
                return response['message']
            results[node['name']] = response["message"]
        return results

    def set_mood(self, mood_data: Dict, nodes: List = None) -> List:
        """
        *mood_data* should be of the format:
            {node-name: {emotive-1: value, emotive-2: value}}

        where node-name is the *name* of a primitive or manipulative.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        results = {}
        if nodes is None:
            nodes = [node['name'] for node in self.all_nodes]
        else:
            nodes = [node for node in self.all_nodes if (node['name'] in nodes)]
        for node in nodes:
            response = requests.post(f"{self.url}{node['id']}/mood/set", verify=self.secure,
                                     headers=self.headers, json={'data': mood_data}).json()
            if 'error' in response or response["status"] == 'failed':
                if len(nodes) == 1 and self.summarize_for_single_node:
                    raise Exception("Request Failure:", response)
                self.failures.append({node['name']: response})
                print("Failure:", {node['name']: response})
            if len(nodes) == 1 and self.summarize_for_single_node:
                return response['message']
            results[node['name']] = response["message"]
        return results

    def analyze_kb(self, nodes: List = None) -> List[Dict[str, Any]]:
        """
        Kickstarts analysis for the selected primitives' KBs.
        This is a long running process and can be monitored via kb_analysis_progress ('/kb/analysis-progress')
        """
        if nodes is None:
            nodes = self.all_nodes
        return self._query(requests.post, 'kb/analyze', nodes=nodes)

    def kb_analysis_progress(self):
        """
        Monitors the KB analysis progress kickstarted by analyze_kb.
        """
        if not self._connected:
            raise ConnectionError(
                'Not connected to a bottle. You must call `connect()` on a BottleClient instance before making queries')
        response = requests.get(f'{self.url}kb/analysis-progress', verify=self.secure, json=[],
                                headers=self.headers).json()
        return response

    def set_target_class(self, target_class: str, nodes: List = None) -> List:
        """Provide a target_class symbol for the searcher to look for. It will ignore all other classes.
        This is a symbol that is in the last event of a classification sequence."""
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'set-target-class', nodes=nodes, data=target_class)

    def clear_target_class(self, nodes: List = None) -> List:
        "Clears target selection."
        if nodes is None:
            nodes = self.query_nodes
        return self._query(requests.post, 'clear-target-class', nodes=nodes)
