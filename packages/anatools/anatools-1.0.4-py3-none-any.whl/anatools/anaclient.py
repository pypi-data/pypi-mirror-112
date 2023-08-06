"""AnaClient is a python module for accessing Rendered.AI's Ana Platform API."""

class AnaClient:

    def __init__(self, workspace=None, environment='prod', verbose=False, email=None, password=None):
        import pyrebase, getpass, time, requests, base64, json, traceback
        import anatools.envs as envs
        self.verbose = verbose
        if environment not in ['dev','test','prod','infra']: 
            print('Invalid environment argument, must be \'infra\', \'dev\', \'test\' or \'prod\'.')
            return None
        self.__environment = environment
        encodedbytes = envs.envs.encode('ascii')
        decodedbytes = base64.b64decode(encodedbytes)
        decodedenvs = json.loads(decodedbytes.decode('ascii'))
        envdata = decodedenvs[environment]
        self.__firebase = pyrebase.initialize_app(envdata)
        self.__url = envdata['graphURL']
        self.__auth = self.__firebase.auth()
        self.__timer = int(time.time())
        self.email = email
        self.__password = password
        
        loggedin = False
        if not self.email:
            print(f'Enter your credentials for the {envdata["name"]}.') 
            self.email = input('Email: ')
        if not self.__password:
            failcount = 1
            while not loggedin:
                self.__password = getpass.getpass()
                try:
                    self.__user = self.__auth.sign_in_with_email_and_password(self.email, self.__password)
                    loggedin = True
                except:
                    if failcount < 5:
                        print('\rInvalid password, please enter your password again.')
                        failcount += 1
                    else:
                        print(f'\rInvalid password, consider resetting your password at {envdata["website"]}/forgot-password.')
                        return
        if not loggedin:
            try:
                self.__user = self.__auth.sign_in_with_email_and_password(self.email, self.__password)
                loggedin = True
            except:
                if self.verbose == 'debug': traceback.print_exc()
                print(f'Failed to login to {envdata["name"]} with email ({email}).')
                return
  
        self.__uid = self.__user['localId']
        self.__headers = {'uid':self.__uid, 'idtoken':self.__user['idToken']}
        self.__logout = False
        if self.verbose == 'debug': print(self.__user['idToken'])
        if workspace:   self.__workspace = workspace
        else:
            response = requests.post(
                url = self.__url, 
                headers = self.__headers, 
                json = {
                    "operationName": "getWorkspaces",
                    "variables": { "uid": self.__uid },
                    "query": """query getWorkspaces($uid: String!) {
                                    getWorkspaces(uid: $uid) {
                                        workspaceid:    id
                                        name:           name
                                        owner:          owner
                                    }
                                }""" })
            if self.verbose == 'debug': print(response.status_code, response.json())
            if response.status_code == 200 and response.json()['data']['getWorkspaces']: 
                workspaces = response.json()['data']['getWorkspaces']
            self.__workspace = workspaces[0]['workspaceid']
            
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getChannels",
                "variables": {
                    "uid": self.__uid 
                    },
                "query": """query getChannels($uid: String!) {
                                getChannels(uid: $uid) {
                                    channelid:  channelID
                                    name:       channelName    
                                }
                            }""" })
        self.__channels = {}
        if response.status_code == 200 and response.json()['data']['getChannels']:
            for channel in response.json()['data']['getChannels']: self.__channels[channel['name']] = channel['channelid']
            if not len(self.__channels.keys()):
                print('No channels found for this user. Contact info@rendered.ai for help with this issue.')
                if self.verbose: print(response.status_code, response.json())   
                return 
        else:
            if self.verbose == 'debug': print(response.status_code, response.json())
            print("Error connecting to endpoint. Contact info@rendered.ai for help with this issue.")
            self.email = None
            return 
        if verbose: print(f'Signed into {envdata["name"]} with {self.email}, using workspace {self.__workspace}.')

    
    def __refresh_token(self):
        import time
        if int(time.time())-self.__timer > int(self.__user['expiresIn']):
            self.__user = self.__auth.sign_in_with_email_and_password(self.email, self.__password)
            self.__headers = {'uid':self.__uid, 'idtoken':self.__user['idToken']}
            self.__timer = int(time.time())


    def __check_logout(self):
        if self.__logout:
            print('You are currently logged out, login to access the Ana tool.')
            return True
        self.__refresh_token()
        return False


    def logout(self, clear=False):
        """Logs out of the ana sdk and removes credentials from Ana.
        """
        if self.__check_logout(): return
        self.email = None
        self.__logout = True
        del self.__password, self.__firebase, self.__url, self.__auth, self.__user, self.__uid, self.__headers, self.__workspace, self.__channels
    

    def login(self, workspace=None, environment='prod', email=None, password=None):
        """Log in to ana sdk 

        Parameters
        ----------
        workspace : str
            ID of the workspace to log in to. Uses default if not specified.
        environment : str
            Environment to log into. Defaults to production.

        """
        self.__init__(workspace, environment, self.verbose, email, password)
        return


    def get_workspace(self):
        """Get workspace id of current workspace. 

        Returns
        -------
        str
            Workspace ID of current workspace.

        """
        if self.__check_logout(): return
        return self.__workspace


    def set_workspace(self, workspaceid=None):
        """Set the workspace to the one you wish to work in.

        Parameters
        ----------
        workspaceid : str
            Workspace ID for the workspace you wish to work in. Uses default workspace if this is not set.

        """
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__uid
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getChannelsWithWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """query getChannelsWithWorkspace($uid: String!, $workspaceId: String!) {
                                getChannelsWithWorkspace(uid: $uid, workspaceId: $workspaceId) {
                                    channelid:  channelID
                                    name:       channelName
                                }
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200: 
            for channel in response.json()['data']['getChannelsWithWorkspace']: self.__channels[channel['name']] = channel['channelid']
            self.__workspace = workspaceid
            return
        else: print('Failed to set workspace.')


    def create_workspace(self, name, channels, description=None):
        """Create a new workspace with specific channels.

        Parameters
        ----------
        name : str    
            New workspace name.
        channels : list
            List of channels to add to workspace. 
        description: str
            Workspace description.

        Returns
        -------
        str
            Workspace ID if creation was successful. Otherwise returns message.

        """    
        import requests
        if self.__check_logout(): return
        if name is None: name = self.__uid
        if description is None: description = ''
        channelids = [self.__channels[channel] for channel in channels]
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceName": name,
                    "channels": channelids,
                    "description": description },
                "query": """mutation createWorkspace($uid: String!, $workspaceName: String!, $channels: [String]!, $description: String!) {
                                createWorkspace(uid: $uid, workspaceName: $workspaceName, channels: $channels, description: $description) {
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createWorkspace']:
            print(response.json())
            return response.json()['data']['createWorkspace']['id']
        else: print('Failed to create the new workspace.')


    def delete_workspace(self, workspaceid=None):
        """Delete an existing workspace. 

        Parameters
        ----------
        workspaceid : str    
            Workspace ID for workspace to get deleted.

        Returns
        -------
        str
            Success or failure message if workspace was sucessfully removed.

        """   
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__workspace 
        response = input('This will remove any configurations, graphs and datasets associated with this workspace.\nAre you certain you want to delete this workspace? (y/n)  ')
        if response not in ['Y', 'y', 'Yes', 'yes']: return
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspace",
                "variables": { 
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """mutation deleteWorkspace($uid: String!, $workspaceId: String!) {
                                deleteWorkspace(uid: $uid, workspaceId: $workspaceId)
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspace']: 
            return response.json()['data']['deleteWorkspace'].lower() == 'success'
        else: print("Failed to delete workspace.")


    def update_workspace(self, description, workspaceid=None):
        """Update workspace description.

        Parameters
        ----------
        description : str    
            New description to replace old one.
        workspaceid : str    
            Workspace ID for workspace to update.

        Returns
        -------
        str
            Success or failure message if workspace description was sucessfully updated.

        """  
        import requests
        if self.__check_logout(): return
        if description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "description": description },
                "query": """mutation updateWorkspace($uid: String!, $workspaceId: String!, $description: String!){
                                updateWorkspace(uid: $uid, workspaceId: $workspaceId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspace']:
            return response.json()['data']['updateWorkspace'].lower() == 'success'
        else: print('Failed to update the workspace description.')
    
    
    def get_workspaces(self):
        """Shows list of workspaces with id, name, and owner data.

        Returns
        -------
        dict
            Workspace data for all workspaces for a user.

        """  
        import requests
        if self.__check_logout(): return
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaces",
                "variables": { "uid": self.__uid },
                "query": """query getWorkspaces($uid: String!) {
                                getWorkspaces(uid: $uid) {
                                    workspaceid:    id
                                    name:           name
                                    owner:          owner
                                }
                            }""" })
        self.__channels = {}
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaces']: 
            return response.json()['data']['getWorkspaces']
        else: print('Failed to get workspaces.')    


    def get_members(self, workspaceid=None):
        """Show workspace members.

        Parameters
        ----------
        workspaceid : str    
            Workspace ID for showing member list. Uses default workspace if not specified. 

        Returns
        -------
        list
            List of members emails that belong to a workspace. 

        """  
        import requests
        if self.__check_logout(): return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid },
                "query": """query getWorkspaceMembers($uid: String!, $workspaceId: String!){
                                getWorkspaceMembers(uid: $uid, workspaceId: $workspaceId){
                                    email: userEmail
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceMembers']:
            return [member['email'] for member in response.json()['data']['getWorkspaceMembers']]
        else: print('Failed to query workspace members.')


    def add_members(self, members, workspaceid=None):
        """Add members to an existing workspace.

        Parameters
        ----------
        members : str or list
            Single or list of members email to add.
        workspaceid : str    
            Workspace ID to add members to. Adds to default workspace if not specified. 

        Returns
        -------
        str
            Response status if members got added to workspace succesfully. 

        """
        import requests
        if self.__check_logout(): return
        if members is None: return
        if type(members) is str: members = [members]
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "members": members},
                "query": """mutation createWorkspaceMembers($uid: String!, $workspaceId: String!, $members: [String]!){
                                createWorkspaceMembers(uid: $uid, workspaceId: $workspaceId, members: $members)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createWorkspaceMembers']:
            return response.json()['data']['createWorkspaceMembers']
        else: print('Failed to add new members to workspace.')


    def remove_members(self,members, workspaceid=None):
        """Remove members from an existing workspace.

        Parameters
        ----------
        members : str or list
            Single or list of members email to remove.
        workspaceid : str    
            Workspace ID to remove members from. Removes from default workspace if not specified. 

        Returns
        -------
        str
            Response status if members got removed from workspace succesfully. 

        """
        import requests
        if self.__check_logout(): return
        if members is None: return
        if type(members) is str: members = [members]
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceMembers",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "members": members},
                "query": """mutation deleteWorkspaceMembers($uid: String!, $workspaceId: String!, $members: [String]!){
                                deleteWorkspaceMembers(uid: $uid, workspaceId: $workspaceId, members: $members)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceMembers']:
            return response.json()['data']['deleteWorkspaceMembers']
        else: print('Failed to delete new members to workspace.')


    def get_channels(self):
        """Shows all channel names. 

        Returns
        -------
        list
            List of all possible channel names.

        """
        if self.__check_logout(): return
        return [key for key in self.__channels.keys()]

    
    def get_graphs(self, graphid=None, name=None, owner=None, workspaceid=None):
        """Queries the workspace graphs based off provided parameters. Checks on graphid, name, or owner in this respective order within the specified workspace.
        If only workspace ID is provided, this will return all the graphs in a workspace. 

        Parameters
        ----------
        graphid : str
            GraphID to filter on. Optional.
        name : str
            Name of the graph to filter on. Optional.
        owner: str
            Owner of graphs to filter on. Optional.
        workspaceid : str    
            Workspace ID to filter on. If none is provided, the default workspace will get used. 
        
        Returns
        -------
        list
            A list of graphs based off provided query parameters if any parameters match.

        """
        import requests
        if self.__check_logout(): return
        if graphid is None: graphid = ''
        if name is None: name = ''
        if owner is None: owner = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceGraphs",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "member": owner,
                    "name": name },
                "query": """query getWorkspaceGraphs($uid: String!, $workspaceId: String!, $graphId: String!, $member: String!, $name: String!){
                                getWorkspaceGraphs(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, member: $member, name: $name){
                                    graphid:        graphid
                                    name:           name
                                    serial:         sn
                                    channel:        channel
                                    owner:          user
                                    description:    description
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceGraphs']:
            return response.json()['data']['getWorkspaceGraphs']
        else: 
            print('Failed to query graphs.')
            return []

    
    def create_graph(self, name, channel, graph, workspaceid=None):
        """Generates a new graph based off provided parameters. 

        Parameters
        ----------
        name : str
            Graph name that will get generated.
        channel: str
            Name of the channel to use for the graph.
        graph: json
            Location of yaml file. Check out the readme for more details (step 3 for how to use ana)
        workspaceid : str    
            Workspace ID create the graph in. If none is provided, the default workspace will get used. 
        
        Returns
        -------
        str
            The graph id if it was created sucessfully or an error message.

        """
        import requests, json
        if self.__check_logout(): return
        if name is None or channel is None or graph is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "channelId": self.__channels[channel],
                    "graph": json.dumps(graph),
                    "name": name },
                "query": """mutation createGraph($uid: String!, $workspaceId: String!, $channelId: String!, $graph: String!, $name: String!){
                                createGraph(uid: $uid, workspaceId: $workspaceId, channelId: $channelId, graph: $graph, name: $name){
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createGraph']:
            return response.json()['data']['createGraph']['id']
        else: print('Failed to create the new graph.')

    
    def update_graph(self, graphid, description, workspaceid=None):
        """Update graph description. 

        Parameters
        ----------
        graphid : str
            Graph id to update.
        description: str
            New description to update.
        workspaceid : str    
            Workspace ID of the graph's workspace. If none is provided, the default workspace will get used. 
        
        Returns
        -------
        str
            A success or error message based on graph's update.

        """
        import requests
        if self.__check_logout(): return
        if graphid is None or description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspaceGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "description": description },
                "query": """mutation updateWorkspaceGraph($uid: String!, $workspaceId: String!, $graphId: String!, $description: String!){
                                updateWorkspaceGraph(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspaceGraph']:
            return response.json()['data']['updateWorkspaceGraph'].lower() == 'success'
        else: print('Failed to update the graph description.')


    def delete_graph(self, graphid, workspaceid=None):
        """Delete a graph in a workspace.

        Parameters
        ----------
        graphid : str
            Graph id to delete.
        workspaceid : str    
            Workspace ID of the graph's workspace. If none is provided, the default workspace will get used. 
        
        Returns
        -------
        str
            A success or error message based on graph's delete.

        """
        import requests
        if self.__check_logout(): return
        if graphid is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceGraph",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid},
                "query": """mutation deleteWorkspaceGraph($uid: String!, $workspaceId: String!, $graphId: String!){
                                deleteWorkspaceGraph(uid: $uid, workspaceId: $workspaceId, graphId: $graphId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceGraph']:
            return response.json()['data']['deleteWorkspaceGraph'].lower() == 'success'
        else: print('Failed to delete the graph.')

    
    def download_graph(self, graphid, workspaceid=None):
        """Download a graph.

        Parameters
        ----------
        graphid : str
            Graph ID of the graph to download.
        workspaceid : str    
            Workspace ID of the graph's workspace. If none is provided, the default workspace will get used. 
        
        Returns
        -------
        str
            A download URL that can be used in the browser or a failure message.

        """
        import requests, json
        if self.__check_logout(): return
        if graphid is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceGraphs",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "member": '',
                    "name": '' },
                "query": """query getWorkspaceGraphs($uid: String!, $workspaceId: String!, $graphId: String!, $member: String!, $name: String!){
                                getWorkspaceGraphs(uid: $uid, workspaceId: $workspaceId, graphId: $graphId, member: $member, name: $name){
                                    graph:          graph
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceGraphs']:
            return json.loads(response.json()['data']['getWorkspaceGraphs'][0]['graph'])
        else: print('Failed to find graph.')

    
    def get_datasets(self, datasetid=None, name=None, owner=None, status=None, workspaceid=None):
        """Queries the workspace datasets based off provided parameters. Checks on datasetid, name, owner, or status in this respective order within the specified workspace.
        If only workspace ID is provided, this will return all the graphs in a workspace. 

        Parameters
        ----------
        datasetid : str
            Graph ID of the graph to download.
        name : str 
            Dataset name.   
        owner: str
            Owner of the dataset.
        status:
            Status of a dataset, whether it is running, completed, stopped, etc. 
        workspaceid : str
            Workspace ID of the graph's workspace. If none is provided, the default workspace will get used. 


        Returns
        -------
        str
            Information about the dataset based off the query parameters provided or a failure message. 

        """
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid = ''
        if name is None: name = ''
        if owner is None: owner = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getWorkspaceDatasets",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid,
                    "member": owner,
                    "name": name },
                "query": """query getWorkspaceDatasets($uid: String!, $workspaceId: String!, $datasetId: String!, $member: String!, $name: String!){
                                getWorkspaceDatasets(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId, member: $member, name: $name){
                                    datasetid:          datasetid
                                    serial:             serial
                                    owner:              user
                                    channel:            channel
                                    description:        description
                                    status:             status
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getWorkspaceDatasets']:
            if status:
                datasets = [dataset for dataset in response.json()['data']['getWorkspaceDatasets'] if dataset['status'] == status]
                return datasets
            else: return response.json()['data']['getWorkspaceDatasets']
        else: 
            print('Failed to query datasets.')
            return []



    def create_dataset(self, name, graphid, description=None, interpretations=1, priority=1, seed=1, workspaceid=None):
        """Create a new dataset based off an existing graph. This will start a new job.

        Parameters
        ----------
        graphid : str
            Graph ID of the graph to create dataset from.
        description : str 
            Description for new dataset.
        interpretations : int
            Number of interpretations.
        priority : int
            Job priority.
        seed : int
            Seed number.
        workspaceid : str
            Workspace ID of the graph's workspace. If none is provided, the default workspace will get used. 


        Returns
        -------
        str
            Success or failure message about dataset creation.

        """
        import requests
        if self.__check_logout(): return
        if name is None or graphid is None: return
        if description is None: description = ''
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createJobWithUserVersion",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "graphId": graphid,
                    "dataset": name,
                    "interpretations": interpretations,
                    "description": description,
                    "priority": priority,
                    "seed": seed },
                "query": """mutation createJobWithUserVersion($uid: String!, $workspaceId: String!, $dataset: String!, $description: String!, $graphId: String!, $interpretations: String!, $priority: String!, $seed: String!) {
                                createJobWithUserVersion(uid: $uid, workspaceId: $workspaceId, dataset: $dataset, description: $description, graphId: $graphId, interpretations: $interpretations, priority: $priority, seed: $seed) {
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createJobWithUserVersion']:
            return response.json()['data']['createJobWithUserVersion']['id']
        else: print('Failed to create the new dataset.')

    
    def update_dataset(self, datasetid, description, workspaceid=None):
        """Update dataset description.

        Parameters
        ----------
        datasetid : str
            Dataset ID to update description for.
        description : str 
            New description.
        workspaceid : str
            Workspace ID of the dataset to get updated. If none is provided, the default workspace will get used. 


        Returns
        -------
        str
            Success or failure message about dataset update.

        """
        import requests
        if self.__check_logout(): return
        if datasetid is None or description is None: return
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "updateWorkspaceDataset",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid,
                    "description": description },
                "query": """mutation updateWorkspaceDataset($uid: String!, $workspaceId: String!, $datasetId: String!, $description: String!){
                                updateWorkspaceDataset(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId, description: $description)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['updateWorkspaceDataset']:
            return response.json()['data']['updateWorkspaceDataset'].lower() == 'success'
        else: print('Failed to update the dataset description.')


    def delete_dataset(self, datasetid, workspaceid=None):
        """Delete an existing dataset.

        Parameters
        ----------
        datasetid : str
            Dataset ID of dataset to delete.
        workspaceid : str
            Workspace ID that the dataset is in. If none is provided, the default workspace will get used. 


        Returns
        -------
        str
            Success or failure message about dataset deletion.

        """
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deleteWorkspaceDataset",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceid,
                    "datasetId": datasetid},
                "query": """mutation deleteWorkspaceDataset($uid: String!, $workspaceId: String!, $datasetId: String!){
                                deleteWorkspaceDataset(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deleteWorkspaceDataset']:
            return response.json()['data']['deleteWorkspaceDataset'].lower() == 'success'
        else: print('Failed to delete the dataset.')


    def download_dataset(self, datasetid, workspaceid=None):
        """Download a dataset.

        Parameters
        ----------
        datasetid : str
            Dataset ID of dataset to download.
        workspaceid : str
            Workspace ID that the dataset is in. If none is provided, the default workspace will get used. 


        Returns
        -------
        str
            Success or failure message about dataset download.

        """
        import requests
        if self.__check_logout(): return
        if datasetid is None: datasetid
        if workspaceid is None: workspaceid = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getDownloadDataset",
                "variables": {
                    "uid": self.__uid,
                    "datasetId": datasetid,
                    "workspaceId": workspaceid },
                "query": """mutation getDownloadDataset($uid: String!, $datasetId: String!, $workspaceId: String!) {
                                getDownloadDataset(uid: $uid, datasetId: $datasetId, workspaceId: $workspaceId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['getDownloadDataset']:
            url = response.json()['data']['getDownloadDataset']
            fname = url.split('?')[0].split('/')[-1]
            downloadresponse = requests.get(url=url)
            with open(fname, 'wb') as outfile:
                outfile.write(downloadresponse.content)
            del downloadresponse
            return fname
        else: print('Failed to download the dataset.')


    def register_docker(self, channel):
        """Register the docker image of a channel.

        Parameters
        ----------
        channel : str
            Channel name for the docker image, this must match the channel docker image.
        
        Returns
        -------
        str
            Success or failure message about docker registration.

        """
        import requests, docker, base64, json, time
        import anatools.envs as envs
        if self.__environment != 'dev': 
            print('Docker containers can only be registered in the Development environment.')
            return False
        if self.__check_logout(): return
        if channel is None: return False
        encodedbytes = envs.envs.encode('ascii')
        decodedbytes = base64.b64decode(encodedbytes)
        decodedenvs = json.loads(decodedbytes.decode('ascii'))
        envdata = decodedenvs[self.__environment]
        
        # check if channel image is in docker
        dockerclient = docker.from_env()
        try: channelimage = dockerclient.images.get(channel)
        except docker.errors.ImageNotFound:
            print('Could not find Docker image with name {channel}.')
            return False
        except:
            print('Error connecting to Docker.')
            return False
        
        # get ecr password
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannelDocker",
                "variables": {
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannelDocker($channelId: String!) {
                                registerChannelDocker(channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerChannelDocker']:
            encodedpass = response.json()['data']['registerChannelDocker']
            encodedbytes = encodedpass.encode('ascii')
            decodedbytes = base64.b64decode(encodedbytes)
            decodedpass = decodedbytes.decode('ascii').split(':')[-1]
        else: 
            print('Failed to retrieve Docker credentials.')
            return

        # tag and push image
        print(f"Pushing {channel} Docker Image. This could take awhile...", end='')
        time.sleep(1)
        reponame = envdata['ecrURL'].replace('https://','')+'/'+channel
        resp = channelimage.tag(reponame)
        if self.verbose == 'debug': print( dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass}) )
        else: resp = dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass})
        print("Complete!")

        # confirm image pushed / start registration
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannel",
                "variables": {
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannel($channelId: String!) {
                                registerChannel(channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        docker_registered = False
        if response.status_code == 200 and response.json()['data']['registerChannel']:
            if response.json()['data']['registerChannel'] == 'success': docker_registered = True
        if not docker_registered: print('Failed to confirm Docker upload.')

        # cleanup docker
        resp = dockerclient.images.remove(reponame)
        return docker_registered

    
    def register_channel_owner(self, email, channel):
        """Set a channel owner. 

        Parameters
        ----------
        email : str
            Email adress for setting the channel owner to.
        channel : str
            Channel name to set the owner for.
        
        Returns
        -------
        bool
            True if channel owner was registered successfully, false otherwise.

        """
        import requests, json
        if email is None or channel is None: return False
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerChannelOwner",
                "variables": {
                    "email": email, 
                    "channelId": self.__channels[channel] },
                "query": """mutation registerChannelOwner($email: String!, $channelId: String!) {
                                registerChannelOwner(email: $email, channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerChannelOwner'] == "success":
            return True
        else: 
            print('Failed to register owner.')
            return False


    def register_package_data(self,package,location):
        """Upload a folder to be available for use with a channel. This is used when uploading multiple files. 

        Parameters
        ----------
        package : str
            Folder name of the package inside the location parameter.
        location : str
            Local directory to search in for the package. It is the path to the package folder.
        
        Returns
        -------
        str
            Succes or error message about package upload.

        """
        # blocked 
        # https://bitbucket.org/renderedai/infra/src/main/infrastructure/graphql/resolvers/services/registerPackageData.ts
        # location = path to packages
        # package = example
        # rename to register_package_data
        # use box.blend and check if it copied to s3. clean up other files except box.blend 
        # Create "example", verify box.blend copied into it. Try a bigger file (1G) to fiugre out copy limit, provide internet speed 
        # result of test: Error with response and upload did not happen
        
        import requests, os, json

        # make sure the package data is 
        if package not in os.listdir(location):
            print(f"Incorrect location of package: {os.listdir(location)}")
            return
        fileroot = os.path.abspath(os.path.join(location,package))

        uploadfiles = []

        # recursively search directory for upload files
        for root, dirs, files in os.walk(fileroot):
            for upfile in files:
                uploadfiles.append(os.path.join(root,upfile))
        
        # for each file, generate a presigned-url and upload via requests
        numfiles = len(uploadfiles)
        getkey = None
        presignedurl = None
        #TODO add more outputs to check graphql works and if presigned url process works
        for i,filepath in enumerate(uploadfiles):
            filename = filepath.split('/')[-1]
            print(f'Uploading file {i} of {numfiles}:    {filename}', end='/r')
            key = filepath.replace(fileroot,'').replace(filename,'')
            if getkey != key:
                getkey = key
                response = requests.post(
                    url = self.__url, 
                    headers = self.__headers, 
                    json = {
                        "operationName": "registerPackageData", #returns presignedurl for location to upload daata to
                        "variables": {
                            "package": package, 
                            "key": key },
                        "query": """mutation registerPackageData($package: String!, $key: String!) {
                                        registerPackageData(package: $package, key: $key)
                                    }""" })
                if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
                if response.status_code == 200 and response.json()['data']['registerPackageData']:
                    presignedurl = response.json()['data']['registerPackageData']
                
            # upload the file
            # check if this works, check in with Ethan if it does not work
            # look at https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html

            with open(filepath, 'rb') as data: #had to change this from filename to filepath for it to get past this step
                files = {'file': (filepath, data)}
                print(files)
                response = requests.post(presignedurl, data=presignedurl['fields'], files=files)
                if response.status_code != 204: 
                    print('Upload failed.')
                    return
        print('Upload complete!')    


    def register_datafile(self,package,filepath):
        """Upload single data file to be available for use with a channel.

        Parameters
        ----------
        package : str
            File name.
        filepath : str
            Local directory to search in for the filename. It is the path to the filename.
        
        Returns
        -------
        str
            Succes or error message about file upload.

        """
        import requests, os
        key = filepath.split(f'/packages/{package}/')[-1]
        filename = key.split('/')[-1]
        key = key.replace(filename,'')
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "registerPackageData",
                "variables": {
                    "package": package, 
                    "key": key },
                "query": """mutation registerPackageData($package: String!, $key: String!) {
                                registerPackageData(package: $package, key: $key)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['registerPackageData']['url']:
            presignedurl = response.json()['data']['registerPackageData']['url']

        with open(filepath, 'rb') as data:
            files = {'file': (filename, data)}
            response = requests.post(presignedurl['url'], data=presignedurl['fields'], files=files)
            if response.status_code != 204: 
                print('Upload failed.')
                return
        print('Upload complete!') 


    def create_channel(self, channel, packages=None, instance=None, organizations=None):
        """Create a new channel.

        Parameters
        ----------
        channel : str
            Name of new channel.
        packages : str
            Package name to use data files from. This is the package that was registered.
        instance: str
            The EC2 instance the channel runs on (ie. p2.xlarge)
        organizations: list
            Organization list for which this channel must belong to.
        Returns
        -------
        str
            Succes or error message about channel creation.

        """
        import requests
        if channel is None or instance is None: 
            print('Must provide channel and instance type.')
            return
        if packages is None: packages = []
        if organizations is None: organizations = []
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createChannel",
                "variables": {
                    "name": channel, 
                    "packages": packages,
                    "instance": instance,
                    "organizations": organizations },
                "query": """mutation createChannel($name: String!, $packages: [String!], $instance: String!, $organizations: [String!]) {
                                createChannel(name: $name, packages: $packages, instance: $instance, organizations: $organizations)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['createChannel']:
            return response.json()['data']['createChannel']
        return False


    def deploy_channel(self, channel, environment='test'):
        """Deploy a channel between environments.

        Parameters
        ----------
        channel : str
            Name of channel to deploy.
        environment : str
            Environment to deploy channel to. 

        Returns
        -------
        str
            Succes or error message about channel deployment.

        """
        import requests
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "deployChannel",
                "variables": {
                    "channelId": self.__channels[channel], 
                    "environment": environment },
                "query": """mutation deployChannel($channelId: String!, $environment: String!) {
                                deployChannel(channelId: $channelId, environment: $environment)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, response.json())
        if response.status_code == 200 and response.json()['data']['deployChannel'] == "success":
            return True
        return False


    def invite_user_to_workspace(self, email, workspaceId=None):
        """Invite a new or existing user to a workspace. This will send the user an email with the invite.

        Parameters
        ----------
        email : str
            Email of user to send invite to.
        workspaceId : str
            Workspace ID to invite user to. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            Succes or error message about invite creation.

        """
        import requests
        import json
        if self.__check_logout(): return
        if email is None: 
            print("No email provided.")
            return 
        if workspaceId is None: workspaceId = self.__workspace
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "inviteUserToWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "email": email,
                    "workspaceId": workspaceId},
                "query": """mutation inviteUserToWorkspace($uid: String!, $email: String!, $workspaceId: String!){
                                inviteUserToWorkspace(uid: $uid, email: $email, workspaceId: $workspaceId){
                                    id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['inviteUserToWorkspace']['id']:
            print(email + ' was sent an invite to the workspace. Invite ID is: ' + response.json()['data']['inviteUserToWorkspace']['id'])
            return
        else:
            print('Failed to create invite.')

    def add_workspace_channel(self, channel_name, workspaceId=None):
        """Add an existing channel to a workspace.

        Parameters
        ----------
        channel_name : str
            Name of channel to add to workspace.
        workspaceId : str
            Workspace ID to add channel into. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            Succes or error message about adding the channel.

        """
        # blocked by bug
        # not working, it sometimes returns a boolean or it will return channelId so the graphql parsing fails
        #https://bitbucket.org/renderedai/infra/src/main/infrastructure/graphql/resolvers/services/updateWorkspace.ts
        import requests
        import json
        if self.__check_logout(): return
        if not channel_name:
            print('Channel name cannot be blank.')
            return

        if channel_name not in self.__channels: 
            print('Channel name not found.')
            return
        
        channelId = self.__channels[channel_name]
        
        if workspaceId is None: workspaceId = self.__workspace        
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "addWorkspaceChannel",
                "variables": {
                    "uid": self.__uid,
                    "channelId": channelId,
                    "workspaceId": workspaceId},
                "query": """mutation addWorkspaceChannel($workspaceId: String!, $channelId: String!){
                                addWorkspaceChannel(workspaceId: $workspaceId, channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['addWorkspaceChannel']['channelId']:
            print(channelId + 'channel was added to workspace.')
            return
        else:
            print('Failed to add channel.')


    def remove_workspace_channel(self, channel_name, workspaceId=None):
        """Remove an existing channel to a workspace.

        Parameters
        ----------
        channel_name : str
            Name of channel to remove from workspace.
        workspaceId : str
            Workspace ID to remove channel from. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            Succes or error message about removing the channel.

        """
        # blocked by bug
        # same issue as add_workspace_channel
        # https://bitbucket.org/renderedai/infra/src/main/infrastructure/graphql/resolvers/services/updateWorkspace.ts
        #TODO in progress
        import requests
        import json
        if self.__check_logout(): return
        if not channel_name:
            print('Channel name cannot be blank.')
            return

        if channel_name not in self.__channels: 
            print('Channel name not found.')
            return
        
        channelId = self.__channels[channel_name]
        
        if workspaceId is None: workspaceId = self.__workspace        
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "removeWorkspaceChannel",
                "variables": {
                    "uid": self.__uid,
                    "channelId": channelId,
                    "workspaceId": workspaceId},
                "query": """mutation removeWorkspaceChannel($workspaceId: String!, $channelId: String!){
                                removeWorkspaceChannel(workspaceId: $workspaceId, channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['removeWorkspaceChannel']['channelId']:
            print(channelId + 'channel was added to workspace.')
            return
        else:
            print('Failed to remove channel.')

    def accept_invitation_of_workspace(self, invitationId):
        """Accept an invite to a workspace. Once accepted, user will be able to access and use the workspace.

        Parameters
        ----------
        invitationId : str
            Id of invite to accept.

        Returns
        -------
        str
            Succes or error message about accepting invite.

        """
        import requests
        import json
        if self.__check_logout(): return
        if not invitationId: 
            print("No invite ID provided.")
            return 
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "acceptInvitationOfWorkspace",
                "variables": {
                    "uid": self.__uid,
                    "invitationId": invitationId},
                "query": """mutation acceptInvitationOfWorkspace($uid: String!, $invitationId: String!){
                                acceptInvitationOfWorkspace(uid: $uid, invitationId: $invitationId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['acceptInvitationOfWorkspace']:
            return
        else:
            print('Failed to accept invite.')

    def create_package(self, name, location):
        # need to revisit this once lambda policy is updated
        # https://bitbucket.org/renderedai/infra/src/main/infrastructure/graphql/resolvers/services/createPackage.ts
        import requests
        import json
        if self.__check_logout(): return
        if not name or not location: 
            print("Name or location not provided.")
            return 
        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "createPackage",
                "variables": {
                    "name": name,
                    "location": location},
                "query": """mutation createPackage($name: String!, $location: String!){
                                createPackage(name: $name, location: $location)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['createPackage']:
            return True
        else:
            print('Failed to create package.')
            return False


    def generate_annotation(self, datasetId, annotation_format, annotation_map, workspaceId=None):
        """Generate an image annotation for an existing dataset.

        Parameters
        ----------
        datasetId : str
            Dataset ID to generate annotation for.
        annotation_format : str
            Image annotation format. Currently only COCO is supported.
        annotation_map: str
            Image annotation mapping. Currently only afv is supported.
        workspaceId: str
            Workspace ID of the dataset to generate annotation for. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            Succes or error message about generating the annotation.

        """
        import requests
        import json
        if self.__check_logout(): return
        if workspaceId is None: workspaceId = self.__workspace

        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "generateAnnotation",
                "variables": {
                    "workspaceId": workspaceId,
                    "datasetId": datasetId,
                    "format": annotation_format,
                    "map": annotation_map },
                "query": """mutation generateAnnotation($workspaceId: String!, $datasetId: String!, $format: String!, $map: String!){
                                generateAnnotation(workspaceId: $workspaceId, datasetId: $datasetId, format: $format, map: $map){
                                   id
                                }
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['generateAnnotation']:
            return
        else:
            print('Failed to generate annotation.')


    def stop_execution(self, datasetId, workspaceId=None):
        """Stop a running job.

        Parameters
        ----------
        datasetId : str
            Dataset ID of the running job to stop.
        workspaceId: str
            Workspace ID of the running job. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            Succes or error message about stopping the job execution.

        """
        import requests
        import json
        if self.__check_logout(): return
        if not datasetId:
            print('No datasetID provided.')
            return
        if workspaceId is None: workspaceId = self.__workspace

        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "stopExecution",
                "variables": {
                    "uid": self.__uid,
                    "workspaceId": workspaceId,
                    "datasetId": datasetId},
                "query": """mutation stopExecution($uid: String!, $workspaceId: String!, $datasetId: String!){
                                stopExecution(uid: $uid, workspaceId: $workspaceId, datasetId: $datasetId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['stopExecution']:
            return
        else:
            print('Failed to stop execution.')


    def remove_channel_owner(self, email, channel_name):
        """Remove owner of existing channel.

        Parameters
        ----------
        email : str
            Email address of user to remove as a channel owner.
        channel_name: str
            Name of channel.

        Returns
        -------
        str
            Succes or error message about channel owner removal.

        """
        import requests
        import json
        if self.__check_logout(): return
        
        if not channel_name or not email:
            print('Channel name or email cannot be blank.')
            return

        if channel_name not in self.__channels: 
            print('Channel name not found.')
            return

        channelId = self.__channels[channel_name]

        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "removeChannelOwner",
                "variables": {
                    "email": email,
                    "channelId": channelId},
                "query": """mutation removeChannelOwner($email: String!, $channelId: String!){
                                removeChannelOwner(email: $email, channelId: $channelId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['removeChannelOwner']:
            return
        else:
            print('Failed to remove channel owner.')

    
    def download_annotation(self, datasetId, annotationId, workspaceId=None):
        """Download a generated image annotation file.

        Parameters
        ----------
        datasetId : str
            Dataset ID to download image annotation for.
        annotationId : str
            Id of previously generated image annotation. 
        workspaceId: str
            Workspace ID of the dataset to generate annotation for. If none is provided, the default workspace will get used. 

        Returns
        -------
        str
            URL if annotation download was successful or failure message. The URL can be used within a browser to download the image annotation file.

        """
        import requests
        import json
        if self.__check_logout(): return
        if workspaceId is None: workspaceId = self.__workspace

        response = requests.post(
            url = self.__url, 
            headers = self.__headers, 
            json = {
                "operationName": "getDownloadAnnotation",
                "variables": {
                    "uid": self.__uid,
                    "datasetId": datasetId,
                    "annotationId": annotationId,
                    "workspaceId": workspaceId },
                "query": """mutation getDownloadAnnotation($uid: String!, $datasetId: String!, $annotationId: String!, $workspaceId: String!){
                                getDownloadAnnotation(uid: $uid, datasetId: $datasetId, annotationId: $annotationId, workspaceId: $workspaceId)
                            }""" })
        if self.verbose == 'debug': print(response.status_code, json.dumps(response.json(), indent=4))
        if response.status_code == 200 and response.json()['data']['getDownloadAnnotation']:
            print(response.json()['data']['getDownloadAnnotation'])
            return
        else:
            print('Failed to download annotation.')
