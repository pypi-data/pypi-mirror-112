import pandas as pd
import numpy as np
import requests
import json

base_url = 'https://www.cloudpandas.com/api/'

class AdminClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = base_url
        self.redis = self.RedisDump(self.api_token, self.base_url)
    
    class RedisDump:
        def __init__(self, api_token, base_url):
            self.api_token = api_token
            self.base_url = base_url
        def list(self):
            url = '{}adminredisdump'.format(self.base_url)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            providers = requests.get(url, headers=headers)
            if providers.status_code == 200:
                return(pd.read_json(providers.json()))
            else:
                raise SystemExit("Error {} - {}:  {}".format(providers.status_code, providers.reason, json.loads(providers.content)))
            

def df_to_json(df):
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].astype('str')
    return(df.to_json())


class Client:
    """A Class used to create a client object for communicating with the API
    
    Attributes
    ----------
    api_token : str
        Your API Authentication token 
    base_url : str
        Base URL for the API
    dataproviders : obj
        An instance of the DataProviders Class initialized with the api_token and base_url from the Client class
    sheets : obj
        An instance of the Sheets Class initialized with the api_token and base_url from the Client class
    
    Classes
    -------
    DataProviders
        A Class used to get information about the Data Providers configured in your account
    Sheets
        A Class used to interact with sheets/files contained in your Data Providers
    """
    def __init__(self, api_token):
        """
        Parameters
        ----------
        api_token : str
            Your API Authentication token 
        """
        self.api_token = api_token
        self.base_url = base_url
        self.dataproviders = self.DataProviders(self.api_token, self.base_url)
        self.sheets = self.Sheets(self.api_token, self.base_url)
    
    class DataProviders:
        def __init__(self, api_token, base_url):
            """
            Parameters
            ----------
            api_token : str
                Your API Authentication token 
            base_url : str
                Base URL for the API
            """
            self.api_token = api_token
            self.base_url = base_url
        def list(self):
            """A Method to list the Data Provider Instances configured in your account
            
            Returns
            -------
            pandas.DataFrame
                id:  Unique ID used to reference that provider
                name:  The given name of the provider
                provider:  What service the provider connects to 
                status:  a-Active, m-Maintnance, e-Expired
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}providerlist'.format(self.base_url)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            providers = requests.get(url, headers=headers)
            if providers.status_code == 200:
                return(pd.DataFrame(providers.json()))
            else:
                raise RuntimeError("Error {} - {}:  {}".format(providers.status_code, providers.reason, json.loads(providers.content)))
                
        ##############
        def keys(self, provider_id):
            """TEMP For Testing Only
            """
            url = '{}keysget/{}'.format(self.base_url, provider_id)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            providers = requests.get(url, headers=headers)
            if providers.status_code == 200:
                return(providers.json())
            else:
                raise RuntimeError("Error {} - {}:  {}".format(providers.status_code, providers.reason, json.loads(providers.content)))
                
        ##############
    
    
    class Sheets:
        def __init__(self, api_token, base_url):
            """
            Parameters
            ----------
            api_token : str
                Your API Authentication token 
            base_url : str
                Base URL for the API
            """
            self.api_token = api_token
            self.base_url = base_url
            
        def list(self, provider_id):
            """A Method to list the sheets/files of a given Data Provider
            
            Parameters
            ----------
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            
            Returns
            -------
            pandas.DataFrame
                id:  Unique ID used to reference that sheet
                name:  The given name of the sheet
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}filelist/{}'.format(self.base_url, provider_id)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            sheet = requests.get(url, headers=headers)
            if sheet.status_code == 200:
                return(pd.read_json(sheet.json()))
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
                
        def get(self, provider_id, sheet_id, sub_sheet=0, skip_rows=0):
            """A Method to get the contents of a sheet/file
            
            Parameters
            ----------
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            sheet_id : str
                The ID or Name of the sheet/file.  ID is more deterministic and thus preferred, but Name will also work. 
                If more than one sheet share the same name, then the most recently modified will be chosen.  
            sub_sheet : int|str
                For files that support sub sheets, such as the sheets within an Excel file, allows a specific sub sheet to be chosen.  
                Input options are the index number (defaults to 0, the first sheet in the workbook) or the name.  
            skip_rows : int
                Allows header rows to be skipped.  Defaults to 0.  
                
            Returns
            -------
            pandas.DataFrame
                Contents of the file chosen, returned as a Pandas DataFrame.  
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}fileget/{}/{}/?sub_sheet={}&skip_rows={}'.format(self.base_url, provider_id, sheet_id, sub_sheet, skip_rows)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            sheet = requests.get(url, headers=headers)
            if sheet.status_code == 200:
                return(pd.read_json(sheet.json()))
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
                
        def info(self, provider_id, sheet_id):
            """A Method to get information about a sheet/file
            
            Parameters
            ----------
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            sheet_id : str
                The ID or Name of the sheet/file.  ID is more deterministic and thus preferred, but Name will also work. 
                If more than one sheet share the same name, then the most recently modified will be chosen. 
                
            Returns
            -------
            dict
                name : str
                    Name of the sheet/file
                id : str
                    Unique ID of the sheet/file
                modified_at : str
                    Datetime string of time last modified
                sub_sheets : list
                    Where supported, Sub Sheets contained in the file
                path/folder : str
                    Where supported, the full path to or folder containing the file
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}fileinfo/{}/{}'.format(self.base_url, provider_id, sheet_id)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            sheet = requests.get(url, headers=headers)
            if sheet.status_code == 200:
                return(sheet.json())
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
                
        def update(self, data, provider_id, sheet_id, sub_sheet='Sheet1'):
            """A Method to update a sheet/file
            
            Parameters
            ----------
            data : pandas.DataFrame
                The data that will be synced to the sheet/file
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            sheet_id : str
                The ID or Name of the sheet/file.  ID is more deterministic and thus preferred, but Name will also work. 
                If more than one sheet share the same name, then the most recently modified will be chosen. 
            sub_sheet : str
                Where supported, the name of the sub sheet.  Defaults to Sheet1
                
            Returns
            -------
            dict
                str
                    OK or Error depending on the success of the operation
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}fileupdate/{}/{}/?sub_sheet={}'.format(self.base_url, provider_id, sheet_id, sub_sheet)
            headers = {'Authorization': 'Token {}'.format(self.api_token), 'Content-Type':'application/json'}
            sheet = requests.post(url, headers=headers, data=df_to_json(data))
            if sheet.status_code == 200:
                return(sheet.json())
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
            
        def create(self, data, provider_id, sheet_name, sub_sheet='Sheet1', sheet_type='sheet', folder_path='0'):
            """A Method to update a sheet/file
            
            Parameters
            ----------
            data : pandas.DataFrame
                The data that will be synced to the sheet/file
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            sheet_name : str
                The Name of the sheet/file to be created
            sub_sheet : str
                Where supported, the name of the sub sheet.  Defaults to Sheet1
            sheet_type : str
                What type of object to create. sheet = GoogleSheets or SmartSheets.  xlsx and csv = file.  
            folder_path : str
                Currently only supported with files, not sheets.  Path to the folder in which to create the file.  
                
            Returns
            -------
            dict
                str
                    OK or Error depending on the success of the operation
                
            Raises
            ------
            RuntimeError
                If attempting to set a folder_path for a sheet
            RuntimeError
                If the API returns anything other than Status 200
            """
            if ((sheet_type.lower() == 'sheet') & (folder_path != '0')):
                raise RuntimeError("folder_path cannot be set with sheet_type=sheet")
            url = '{}filecreate/{}/{}/?sub_sheet={}&sheet_type={}&folder_id={}'.format(self.base_url, provider_id, sheet_name, sub_sheet, sheet_type, folder_path)
            headers = {'Authorization': 'Token {}'.format(self.api_token), 'Content-Type':'application/json'}
            sheet = requests.post(url, headers=headers, data=df_to_json(data))
            if sheet.status_code == 200:
                return(sheet.json())
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
                
        def delete(self, provider_id, sheet_id):
            """A Method to remove a sheet/file
            
            Parameters
            ----------
            provider_id : str
                The ID or Name of the Data Provider to use.  ID is more deterministic and thus preferred, but Name will also work. 
            sheet_id : str
                The ID or Name of the sheet/file.  ID is more deterministic and thus preferred, but Name will also work. 
                If more than one sheet share the same name, then the most recently modified will be chosen. 
                
            Returns
            -------
             : str
                 Status message, success or error
                
            Raises
            ------
            RuntimeError
                If the API returns anything other than Status 200
            """
            url = '{}filedelete/{}/{}'.format(self.base_url, provider_id, sheet_id)
            headers = {'Authorization': 'Token {}'.format(self.api_token)}
            sheet = requests.get(url, headers=headers)
            if sheet.status_code == 200:
                return(sheet.json())
            else:
                raise RuntimeError("Error {} - {}:  {}".format(sheet.status_code, sheet.reason, json.loads(sheet.content)))
                
                
                