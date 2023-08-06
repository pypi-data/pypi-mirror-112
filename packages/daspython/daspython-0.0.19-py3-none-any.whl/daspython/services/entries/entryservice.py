

from daspython.common.api import ApiMethods, Token


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
