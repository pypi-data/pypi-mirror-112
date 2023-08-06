# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.
import time
from enum import Enum
import typing
import os
import numpy as np
import pandas as pd
from urllib3.exceptions import MaxRetryError

from shapelets.dsl import (
    SupportedTypes,
    NodeReturnType
)
from shapelets.model import (
    Sequence,
    NDArray,
    Collection,
    CollectionType,
    SequenceMetadata,
    FunctionDescription,
)
from shapelets.services import (
    TestService,
    ExecutionService,
    CollectionsService,
    SequencesService,
    NDArraysService,
    UsersService,
    MetadataService,
    FunctionsService,
    ShapeletsLoginException,
    DataAppService,
    LoginService,
    read_user_from_login_file
)
from shapelets.dsl import DataApp


class Services(Enum):
    TEST = "test_service"
    USERS = "users_service"
    COLLECTIONS = "collections_service"
    SEQUENCES = "sequences_service"
    NDARRAYS = "ndarrays_service"
    METADATA = "metadata_service"
    DATA_APP = "data_app_service"
    EXECUTION = "execution_service"
    FUNCTIONS = "functions_service"


class Shapelets:
    """
    This class is a Shapelets client, it keeps the user session.
    """

    def __init__(self, login_service: LoginService):
        base_url = login_service.base_url
        cookies = login_service.cookies
        self.services = {
            Services.COLLECTIONS: CollectionsService(base_url, cookies),
            Services.SEQUENCES: SequencesService(base_url, cookies),
            Services.NDARRAYS: NDArraysService(base_url, cookies),
            Services.METADATA: MetadataService(base_url, cookies),
            Services.USERS: UsersService(base_url, cookies),
            Services.DATA_APP: DataAppService(base_url, cookies),
            Services.EXECUTION: ExecutionService(base_url, cookies),
            Services.FUNCTIONS: FunctionsService(base_url, cookies),
            Services.TEST: TestService(base_url, cookies)
        }
        self.services[Services.FUNCTIONS].download_dsl()

    # ########################### #
    # CollectionsService methods: #
    # ########################### #

    def create_collection(self,
                          name: str = "",
                          description: str = "",
                          tags: typing.List[str] = None,
                          collection_type: CollectionType = CollectionType.GENERAL) -> Collection:
        """
        This function creates a new collection in Shapelets.
        :param name: A String with the name of the collection.
        :param description: A String which describes the purpose of this collection.
        :param tags: A list of String, that represent the features of this collection.
        :param collection_type: A String to represent the type of this collection.
        :return: A new Shapelets Collection.
        """
        return self.services[Services.COLLECTIONS].create_collection(
            name=name,
            description=description,
            tags=tags,
            collection_type=collection_type)

    def create_default_collections(self, collection_name: str = "ENERNOC") -> None:
        """
        This function creates defaults collections in the Shapelets instance.

        It is a collection with some sequences extracted from the Dataset passed
        as argument, by default ENERNOC.
        :param collection_name: The collection name, ENERNOC as example.
        :return: The default collection of interest.
        """
        self.services[Services.COLLECTIONS].create_default_collections(collection_name)

    def get_collections(self) -> typing.List[Collection]:
        """returns a list of all the user's collections.
        :return: A list of Shapelets Collections.
        """
        return self.services[Services.COLLECTIONS].get_collections()

    def get_collection(self, collection_id):
        """
        This functions returns the collection with the id passed as argument.
        :param collection_id: The collection id.
        :return: A Shapelets Collection.
        """
        return self.services[Services.COLLECTIONS].get_collection(collection_id)

    def update_collection(self,
                          collection,
                          name=None,
                          favorite=None,
                          description=None,
                          tags=None,
                          collection_type=None):
        """
        This function updates a collection with the arguments passed to this function.
        :param collection: The Shapelets Collection.
        :param name: A String with the name of the Collection.
        :param favorite: Boolean to indicate if it is favourite or not.
        :param description: A String with the description of this collection.
        :param tags: A list of Strings with containing the tags f the collection.
        :param collection_type: The collection type.
        :return: The update collection
        """
        return self.services[Services.COLLECTIONS].update_collection(
            collection,
            name=name,
            favorite=favorite,
            description=description,
            tags=tags,
            collection_type=collection_type)

    def delete_collection(self, collection):
        """
        This function deletes a collection.
        :param collection: The Shapelets Collection.
        :return: Returns True if the operation was successful False otherwise.
        """
        return self.services[Services.COLLECTIONS].delete_collection(collection)

    def get_collection_sequences(self, collection: Collection) -> typing.List[Sequence]:
        """
        This function gets all Shapelets Sequences from the Collection
        with collection ID passed as argument.
        :param collection: The Collection
        :return: List of Shapelets Sequences.
        """
        return self.services[Services.COLLECTIONS].get_collection_sequences(collection)

    def get_collection_types(self):
        """
        This function returns a list with all types of collections.
        :return: A list of strings with all sequence types.
        """
        return self.services[Services.COLLECTIONS].get_collection_types()

    def share_collection(self, collection, subject, grant):
        """
        This function shares a collection with the given sid, which can be an user or group
        :param collection: Collection of sequences.
        :param subject: Subject can be an user or group.
        :param grant: The Permission of access.
        """
        self.services[Services.COLLECTIONS].share_collection(collection, subject, grant)

    def unshare_collection(self, collection, subject):
        """
        This function unshares a collection with the given sid, which can be an user or group.
        :param collection: Collection of sequecnes.
        :param subject: Subject, can be an user or group.
        """
        self.services[Services.COLLECTIONS].unshare_collection(collection, subject)

    def get_collection_sharing(self, collection):
        """
        This function returns a List containing the users with access to the given collection.
        :param collection: The collection.
        :return: List of users with access permission.
        """
        self.services[Services.COLLECTIONS].get_collection_sharing(collection)

    def get_collection_privileges(self, collection):
        """
        This function returns a List containing the users with access to the given collection.
        :param collection: The collection.
        :return: List of users with access permission.
        """
        self.services[Services.COLLECTIONS].get_collection_privileges(collection)

    # ######################### #
    # NDArraysService methods: #
    # ######################### #

    def create_nd_array(self,
                        array: np.ndarray,
                        name: str = None,
                        description: str = None) -> NDArray:
        """
        This function registers a new NDArray into Shapelets.
        :param array: The numpy ndarray to be stored.
        :param name: The name of the NDArrray.
        :param description: The description of the NDArray.
        :return: The registered NDArray.
        """
        return self.services[Services.NDARRAYS].create_nd_array(array, name, description)

    def get_nd_array_data(self, ndarray: NDArray) -> np.ndarray:
        """
        This function returns an existing NDArray in Shapelets.
        :param ndarray: The numpy ndarray to be returned.
        :return: The numpy array.
        """
        return self.services[Services.NDARRAYS].get_nd_array_data(ndarray)

    def update_nd_array(self, nd_array: NDArray, array: np.ndarray = None) -> NDArray:
        """
        This function updates a NDArray. This function checks dimensionality to ensure integrity between
        array's data and array's metadata.
        :param nd_array: The NDArray to be updated.
        :param array: This parameter is optional, if present the array's data is update as well..
        :return: The registered NDArray.
        """
        return self.services[Services.NDARRAYS].update_nd_array(nd_array, array)

    def delete_nd_array(self, nd_array: NDArray) -> bool:
        """
        This function deletes the given NDArray.
        :param nd_array: The NDArray to be deleted.
        """
        return self.services[Services.NDARRAYS].delete_nd_array(nd_array)

    # ######################### #
    # SequencesService methods: #
    # ######################### #

    def create_sequence(self,
                        dataframe: pd.DataFrame,
                        name: str = "",
                        starts: np.datetime64 = None,
                        every=None,
                        collection=None) -> Sequence:
        """
        This method creates a sequence from a dataframe and stores it in Shapelets.

        NOTE: Only regular (evenly spaced) series are allowed.

        :param dataframe: A pandas dataframe. If it has a datetime64 index it will be used.
        :param name: name of the sequence.
        :param every: Time in milliseconds for regular series. The parameter is mandatory
            if the dataframe has not a datetime64 index.
        :param starts: Start is the timestamp of the beginning of the sequence. The
            parameter is mandatory if the dataframe has not a datetime64 index.
        :param collection: The collection that sets if the sequence should be add to
            a collection. None if it is not required.
        :return: The sequenceSpec of the sequence.
        """

        if collection is None:
            collections = self.services[Services.COLLECTIONS].get_collections()
            collection = next(
                col for col in collections if col.name == "Default Collection")
        return self.services[Services.SEQUENCES].create_sequence(
            dataframe,
            name,
            starts,
            every,
            collection)

    def update_sequence(self, sequence, dataframe):
        self.services[Services.SEQUENCES].update_sequence(sequence, dataframe)

    def get_sequence_data(self, sequence):
        return self.services[Services.SEQUENCES].get_sequence_data(sequence)

        # ######################## #
        # MetadataService methods: #
        # ######################## #

    def get_metadata(self, collection: Collection) -> pd.DataFrame:
        """
        Get all the metadata for the given Collection
        :param collection:
        :return: A dataframe with all de metadata with sequence names
            as index and each column name as the metadata
        field.
        """
        return self.services[Services.METADATA].get_metadata(collection)

    def add_metadata(self, collection: Collection, sequence: Sequence, metadata: SequenceMetadata):
        """
        Add MetaData to a Sequence in a Collection
        :param collection: The Collection which the sequence belong to.
        :param sequence: The Sequence
        :param metadata: the metadata to add
        :return:
        """
        self.services[Services.METADATA].add_metadata(collection, sequence, metadata)

    def add_metadata_from_pandas(self, collection: Collection, dataframe: pd.DataFrame):
        """
        Add a pandas dataframe with metadata to sequences in a Collection.

        The dataframe has to be of the following shape:
            - It must have an index with the name of the sequences.
            - Each column name will be the metadata name and the value of each
              row will be the value of this metadata for the sequence in the
              index of the row.
        The supported types are:
            - float
            - str
            - datetime.datetime
            - np.datetime64
            - shapelets.MetadataCoordinates
        :param collection: the Collection
        :param dataframe: the dataframe with the metadata
        :return:
        """
        self.services[Services.METADATA].add_metadata_from_pandas(
            collection,
            self.get_collection_sequences(collection),
            dataframe)

    # ##################### #
    # UsersService methods: #
    # ##################### #

    def get_users(self):
        """
        Returns a list os users in the system.
        :return: List of users.
        """
        return self.services[Services.USERS].get_users()

    def get_groups(self):
        """
        Returns a list of groups in the system.
        :return: List of groups.
        """
        return self.services[Services.USERS].get_groups()

    def get_my_user_details(self):
        """
        Returns the calling user details.
        :return: UserDetails
        """
        return self.services[Services.USERS].get_my_user_details()

    def get_user_details(self, subject_id):
        """
        Returns the user details for the given subject.
        :param subject_id: The User.
        :return: an instance of User
        """
        return self.services[Services.USERS].get_user_details(subject_id)

    # ######################### #
    # DataAppService methods: #
    # ######################### #

    def get_data_apps(self) -> typing.List[DataApp]:
        return self.services[Services.DATA_APP].get_data_apps()

    def register_data_app(self, app: DataApp):
        return self.services[Services.DATA_APP].register_data_app(app)

    def delete_data_app(self, data_app_id: str) -> bool:
        return self.services[Services.DATA_APP].delete_data_app(data_app_id)

    # ######################### #
    # ExecutionService methods: #
    # ######################### #

    def run(self, output_nodes: NodeReturnType) -> SupportedTypes:
        return self.services[Services.EXECUTION].run_and_wait_for_all(output_nodes)

    def run_async(self, output_nodes: NodeReturnType) -> int:
        return self.services[Services.EXECUTION].run_async(output_nodes)

    def wait_for_result(self, job_id) -> SupportedTypes:
        return self.services[Services.EXECUTION].wait_for_result(job_id)

    def get_all_analysis(self) -> typing.List[str]:
        return self.services[Services.EXECUTION].get_all_analysis()

    # ######################### #
    # FunctionsService methods: #
    # ######################### #

    def register_custom_function(self,
                                 custom_function: typing.Callable,
                                 description: FunctionDescription = None,
                                 force: bool = True):
        """
        This function registers a new User function in the system.
        :param custom_function: The function to be registered.
        :param description: The description of hte function.
        :param force: Force overwriting the function if there is one
            function with this name already registered.
        :return:
        """
        self.services[Services.FUNCTIONS].register_custom_function(custom_function, description, force)

    def register_custom_splitter(self,
                                 custom_function: typing.Callable,
                                 description: FunctionDescription = None,
                                 force: bool = True):
        """
        This function registers a new Splitter user function in the system.
        :param custom_function: The function to be registered.
        :param description: The description of hte function.
        :param force: Force overwriting the function if there is one function
            with this name alreade registered.
        """
        self.services[Services.FUNCTIONS].register_custom_splitter(custom_function, description, force)

    def register_custom_reducer(self,
                                custom_function: typing.Callable,
                                description: FunctionDescription = None,
                                force: bool = True):
        """
        This function registers a new User function in the system.
        :param custom_function: The function to be registered.
        :param description: The description of hte function.
        :param force: Force overwriting the function if there is one
            function with this name alreade registered.
        """
        self.services[Services.FUNCTIONS].register_custom_reducer(custom_function, description, force)

    def register_flow(self,
                      name: str,
                      output_nodes: NodeReturnType,
                      output_names: typing.Optional[typing.List[str]] = None):
        self.services[Services.FUNCTIONS].register_flow(name, output_nodes, output_names)

    def register_analysis(self,
                          name: str,
                          output_nodes: NodeReturnType,
                          output_names: typing.Optional[typing.List[str]] = None):
        self.services[Services.FUNCTIONS].register_analysis(name, output_nodes, output_names)

    def delete_analysis(self, name: str):
        self.services[Services.FUNCTIONS].delete_analysis(name)

    def delete_all_analysis(self):
        self.services[Services.FUNCTIONS].delete_all_analysis()

    def get_function_parameters(self, name: str = None):
        """
        This function return a FunctionParametersDescription or
        List[FunctionParametersDescription] depending on the
        name parameter. If it is not given, this function will
        return a list of all functions within the system, otherwise
        it will return the FunctionParametersDescription of the
        requested function.
        :param name: The function name to be returned.
        """
        return self.services[Services.FUNCTIONS].get_function_parameters(name)

    # #################### #
    # TestService methods: #
    # #################### #

    def ping(self):
        """
        This function performs a ping action.
        :return True if it receives the pong message.
        """
        return self.services[Services.TEST].ping()

    def test_get(self, api_path):
        return self.services[Services.TEST].test_get(api_path)

    def test_get_raw(self, api_path):
        return self.services[Services.TEST].test_get_raw(api_path)

    def test_delete(self, api_path):
        return self.services[Services.TEST].test_delete(api_path)

    def test_post(self, api_path, data):
        return self.services[Services.TEST].test_post(api_path, data)

    def test_put(self, api_path, data):
        return self.services[Services.TEST].test_put(api_path, data)


def start_shapelet_processes():
    from shapelets.__main__ import start_all_command
    start_all_command()
    login_service = LoginService('https://localhost', 8443)
    while True:
        try:
            login_service.login_user("admin", "admin")
            print(f"server is up...")
            break
        except:
            print(f"server is starting, takes a few seconds...")
            time.sleep(5)


def stop_shapelet_processes():
    from shapelets.__main__ import stop_command
    stop_command()


def close_session():
    stop_shapelet_processes()


def init_session(username: str = None,
                 password: str = None,
                 address: str = "https://localhost",
                 port: int = 8443) -> Shapelets:
    """
    Initializes the session in Shapelets with the given user, password and address.
    :param username:
    :param password:
    :param address:
    :param port:
    :return: The Shapelets object to access all the system API
    """
    start_shapelet_processes()
    if username and password and address:
        print(f"Login as {username} for address {address}")
        login_service = LoginService(address, port)
        login_service.login_user(username, password)
        return Shapelets(login_service)

    if username and address:
        user_info = read_user_from_login_file(address, username)
        if user_info:
            print(f"Found {username} info in login file for address {address}")
            return init_session(
                user_info["user"],
                user_info["password"],
                user_info["server"],
                port)
        elif os.environ.get("SHAPELETS_PWD"):
            print(f"Found {username} info in Env Variable")
            return init_session(
                username,
                os.environ.get("SHAPELETS_PWD"),
                address,
                port)
        else:
            raise ShapeletsLoginException(f"{username} information not found for address {address}")

    if address:
        user_info = read_user_from_login_file(address)
        if user_info:
            print(f"Found default user info in login file for {address}")
            return init_session(
                user_info["user"],
                user_info["password"],
                user_info["server"],
                port)
        elif os.environ.get("SHAPELETS_USER"):
            print("Found user name in Env Variable")
            return init_session(
                os.environ.get("SHAPELETS_USER"),
                None,
                address,
                port)
        else:
            raise ShapeletsLoginException(f"Login information not found for address {address}")
    else:
        raise ShapeletsLoginException("Login information not found")


def update_password(user: str, password: str, new_password: str, address: str, port: int = None):
    """
    Update the password for an user.
    :param user:
    :param password:
    :param new_password:
    :param address:
    :param port:
    :return: True if the password was succesfully updated
    """
    login_service = LoginService(address, port)
    login_service.update_password(user, password, new_password)
    return Shapelets(login_service)
