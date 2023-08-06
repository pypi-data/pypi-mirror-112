import uuid

from requests.api import request
from daspython.common.api import ApiMethods, Token
from daspython.services.attributes.attributeservice import AttributeService
from daspython.services.searches.searchservice import SearchEntriesRequest, SearchService


class InsertRequest():
    '''
    Object with the new entry values.

    Attributes
    ----------
        entry: dictionary
            Reprsents the  { 'field1' : 'value1', 'field2' : 'value2' ... } as an entry content.
    '''
    entry = {}


class UpdateRequest(InsertRequest):
    '''
    Object with the entry values to be updated.

    Attributes
    ----------
        entry: dictionary
            Reprsents the  { 'field1' : 'value1', 'field2' : 'value2' ... } as an entry content.
    '''


class GetEntryRequest():
    '''
    The request object to fetch an entry.

    Attributes
    ----------
        attributeid: int (default None)
            The entry's attribute identifier.
        id: str (default None)
            An entry identifier.
    '''
    attributeid: int = None
    id: str = None


class GetAllEntriesRequest():
    '''
    The request object to fetch a list of entries.

    Attributes
    ----------
        attributeId: int (default None)
            The entries attribute identifier.
        maxresultcount: int (default 10)
            Maximum items expected. The default value is 10.
        sorting: str (default None)                    
            Sorting expression.
                Example: 'displayname asc' --> Sort the result by displayname in ascending order.            
        skipcount: str (default 0)
            Represents the number of items that should be skipped like a page. The default value is 0 which means, combined with the parameter maxresultcount = 10 a page 0 with 10 items.
        attributename: str
            If you don't know the attribute identifier you may use the attribute name instead.
        attributealias: str            
            Other alternative if you don't know either the attribute name or the attribute identifier.
        querystring: str (default None)                    
            Your search filter. 
                Example: 'id(56);displayname(64*)' --> Find the item with a identifier equals 56 and the displayname starts with 64.
    '''
    attributeid: int = None
    maxresultcount: int = 10
    sorting: str = None
    skipcount: int = 0
    attributename: str = None
    attributealias: str = None
    querystring: str = None


class GetEntryRelationsRequest():
    '''
    The request object to fetch a list of entries with either its children or parents.

    Attributes
    ----------
        attributeId: int (default None)
            The entries attribute identifier.
        maxresultcount: int (default 10)
            Maximum items expected. The default value is 10.
        sorting: str (default None)                    
            Sorting expression.
                Example: 'displayname asc' --> Sort the result by displayname in ascending order.            
        skipcount: str (default 0)
            Represents the number of items that should be skipped like a page. The default value is 0 which means, combined with the parameter maxresultcount = 10 a page 0 with 10 items.
        attributename: str
            If you don't know the attribute identifier you may use the attribute name instead.
        attributealias: str            
            Other alternative if you don't know either the attribute name or the attribute identifier.
        querystring: str (default None)                    
            Your search filter. 
                Example: 'id(56);displayname(64*)' --> Find the item with a identifier equals 56 and the displayname starts with 64.
        relationtype: int               
            1 - Parents and 2 - Children.
        deeplevel: int
            Defines the maximum level of relations to be load on your request.            
    '''
    attributeid: int = None
    attributename: str = None
    attributealias: str = None
    attributetablename: str = None
    sorting: str = None
    maxresultcount: int = 10
    skipcount: int = 0
    relationtype: int = 1
    deeplevel: int = 1


class EntryService(ApiMethods):
    def __init__(self, auth: Token):
        super().__init__(auth)

    def get_all(self, request: GetAllEntriesRequest):
        '''
        Get all entries based on the request parameter values.

        Parameters
        ----------
        request : GetAllEntriesRequest
            An instance of the class: GetAllEntriesRequest.

        Returns
        -------
            A json that represents  a list of entries.                           
        '''
        api_url = '/api/services/app/Entry/GetAll?'
        return self.get_data(url=api_url, request=request)

    def get(self, request: GetEntryRequest):
        '''
        Get an entry.

        Parameters
        ----------
        request : GetEntryRequest
            An instance of the class: GetEntryRequest.

        Returns
        -------
            A json that represents  an entry.                           
        '''
        api_url = '/api/services/app/Entry/Get?'
        return self.get_data(url=api_url, request=request)

    def get_entries_level(self, body: GetEntryRelationsRequest):
        '''
        Get all entries based on the body parameter values and includes either its children or parents based on  the given relation type.

        Parameters
        ----------
        request : GetEntryRequest
            An instance of the class: GetEntryRelationsRequest.

        Returns
        -------
            A json that represents a list of entries.                           
        '''
        api_url = '/api/services/app/Entry/GetAllLevels?'
        return self.post_data(url=api_url, body=body)

    def create(self, body: InsertRequest) -> str:
        '''
        Creates a new entry.

        Parameters
        ----------
        body: InsertRequest
            Represents the entry content that will be used to create a new one. Please see also: InsertRequest.

        Returns
        -------
            The new entry's indentifier.
        '''
        body.entry['id'] = str(uuid.uuid1())
        api_url = '/api/services/app/Entry/Create'
        return self.post_data(url=api_url, body=body)

    def update(self, body: UpdateRequest):
        '''
        Updates a new entry.

        Parameters
        ----------
        body: UpdateRequest
            Please see also: UpdateRequest.

        Returns
        -------
            The updated entry's indentifier.
        '''
        api_url = '/api/services/app/Entry/Update'
        return self.put_data(url=api_url, body=body)

    def delete_entry(self, id, attributeId):
        '''
        Deletes an entry.

        id: str
            Enty's identifier. 

        attributeId: int
            Enty's attribute identifier.          

        Returns
        -------
            True if the entry was deleted successfully.
        '''
        api_url = f'/api/services/app/Entry/Delete?Id={id}&AttributeId={attributeId}'
        return self.delete_data(url=api_url)

    def get_entry_id(self, name: str, attribute: str) -> str:
        '''
        Gets the entry identifier based on its name and attribute.

        Parameters
        ----------
            name:str
                Entry's name.
            attribute: str
                Entry's attribute name.

        Returns
        -------
            `str`: Entry identifier.
        '''
        attribute_service = AttributeService(self.token)

        attribute_id = attribute_service.get_attribute_id(attribute)

        if (attribute_id == None):
            return None

        search = SearchService(self.token)
        request = SearchEntriesRequest()
        request.querystring = f'displayname({name})'
        request.maxresultcount = 1
        request.attributeId = attribute_id
        response = search.search_entries(request)

        if (response == None or response['result'] == None or response['result']['totalCount'] == None or response['result']['totalCount'] == 0):
            return None

        return response['result']['items'][0]['entry']['id']
