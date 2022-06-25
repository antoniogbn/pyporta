import requests
import json
import os.path

requests.packages.urllib3.disable_warnings()

class PortaServer(object):
    def __init__(self, h, u, p):
        self.hostname = h
        self.login = u 
        self.password = p         
        self.session_id  = ""
        self._apibase ='https://%s/rest/' % h

    def __str__(self):
        saida = '\n API Server Info >> %s : %s : %s : %s : %s \n' % (self.hostname, self.username, self.password, self.session, self._apibase )
        return saida

    def CallAPI(self,params,resource,debug=0):
        apidata = {'auth_info': json.dumps({'session_id': self.session_id}), 'params': params}
        if debug:
            print(apidata)
        saida = requests.post(self._apibase + resource, data=apidata, verify=False).json()       
        if debug:
            print(saida)
        return saida
        
    def Connect(self):
        req_data = json.dumps({'login':self.login,'password':self.password})
        data = self.CallAPI(req_data, 'Session/login',1)
        self.session_id = data['session_id']
        return data

    def GetAccountList(self,id="",offset=0,limit=1000,i_customer=""):
        req_data =  json.dumps({"id":id,"i_customer":i_customer,"bill_status":"O","get_not_closed_accounts":1,"billing_model":1,"get_only_real_accounts":1,"get_total":0,"limit":limit,"offset":offset})
        data = self.CallAPI(req_data, 'Account/get_account_list')
        return data

    def GetAccountListNoFilter(self,id="",offset=0,limit=1000,i_customer=""):
        req_data =  json.dumps({"id":id,"i_customer":i_customer,"limit":limit,"offset":offset})
        data = self.CallAPI(req_data, 'Account/get_account_list')
        return data

    def GetAccountInfo(self, id, detail=0):
        req_data = json.dumps({"id":id,"detailed_info":detail})
        data = self.CallAPI(req_data,'Account/get_account_info')
        return data

    def GetAccountServicesFeatures(self, id):
        req_data = json.dumps({"i_account":id,"detailed_info":0})
        data = self.CallAPI(req_data,'Account/get_service_features')
        return data

    def GetAccountFollowMe(self, id):
        req_data = json.dumps({"i_account":id})
        data = self.CallAPI(req_data,'Account/get_account_followme')
        return data

    def AddAccountSipInfo(self, customer, account, bmodel, product, sipcld, sipadd, batch):
        service_features = {"flag_value": "Y", "name": "sip_static_contact", "attributes": [{"name": "use_tcp", "values": ["N"]}, { "name": "user","values": [sipcld]}, {"name": "host","values": [sipadd] }]}
        accountinfo = {"id" : account,"billing_model":bmodel,"i_product":product,"i_customer":customer, "h323_password":'E9W5KWgY', "batch_name":batch ,"service_features": [service_features_sip] }
        req_data = json.dumps({"account_info" : accountinfo})
        data = self.CallAPI(req_data, 'Account/add_account')
        return data

    def AddAccount(self, customer, account,password, product, batch,bmodel=1):
        accountinfo = {"id":account,"billing_model":bmodel,"i_product":product,"i_customer":customer, "h323_password":password, "batch_name": batch }
        req_data = json.dumps({"account_info" : accountinfo})
        data = self.CallAPI(req_data, 'Account/add_account',1)
        return data

    def AddCustomer(self, name, curr):
        customerinfo = {"name":name,"iso_4217":curr}
        req_data = json.dumps({"customer_info" : customerinfo})
        data = self.CallAPI(req_data, 'Customer/add_customer')
        return data

    def SetCustomerTrafficLimit(self, customer, tprofile):
        customerinfo = {"i_customer":customer,"i_traffic_profile":tprofile}
        req_data = json.dumps({"customer_info" : customerinfo})
        data = self.CallAPI(req_data, 'Customer/update_customer')
        return data

    def SetCustomField(self, i_customer, i_custom_field, db_value):     
        custom_fields_values  = {"i_custom_field": i_custom_field, "db_value": db_value}
        custom_fields_values  = [custom_fields_values]
        req_data = json.dumps({"i_customer":i_customer, "custom_fields_values": custom_fields_values})
        data = self.CallAPI(req_data, 'Customer/update_custom_fields_values',1)      
        return data

    def SetAccountSipInfo(self, id, sipcld, sipadd):
        service_features = {"flag_value": "Y", "name": "sip_static_contact", "attributes": [{"name": "use_tcp", "values": ["N"]}, { "name": "user","values": [sipcld]}, {"name": "host","values": [sipadd] }]}
        accountinfo = {"i_account" : id,"service_features": [service_features_sip] }
        req_data = json.dumps({"account_info" : accountinfo})
        data = self.CallAPI(req_data, 'Account/update_service_features')
        return data

    def SetFollowMeNumber(self, i_account, redirect_number):
        number_info = {"i_account": i_account, 'redirect_number':redirect_number}
        req_data = json.dumps({"number_info" : number_info})
        data = self.CallAPI(req_data,'Account/add_followme_number')
        return data

    def SetSimpleCallFwd(self, id):
        service_features = {"flag_value": "C", "name": "forward_mode"}
        req_data = json.dumps({"i_account" : id,"service_features": [service_features]})
        data = self.CallAPI(req_data, 'Account/update_service_features')
        return data

    def SetDisableSimpleCallFwd(self, id):
        service_features = {"flag_value": "N","effective_flag_value":"N", "name": "forward_mode"}
        req_data = json.dumps({"i_account" : id,"service_features": [service_features]})
        data = self.CallAPI(req_data, 'Account/update_service_features')
        return data
    
    def SetAccountRoutePlan(self, i_account, routeplan_id):
       account_info = {'detailed_response':0,'i_account':i_account,'service_features':[{'flag_value': "Y", 'name':'individual_routing_plan','attributes':[{'name':'i_routing_plan','values':[ routeplan_id ]}]}]} 
       req_data = json.dumps(account_info)       
       data = self.CallAPI(req_data,'Account/update_service_features')
       return data

    def SetAccountProduct(self, i_account, product_id):
       account_info = {"account_info" : {'i_account':i_account,'i_product':product_id} }
       req_data = json.dumps(account_info)       
       data = self.CallAPI(req_data,'Account/update_account')
       return data

    def GetAccountFollowMe(self, id):
        req_data = json.dumps({"i_account":id})
        data = self.CallAPI(req_data,'Account/get_account_followme')
        return data

    def GetAccountServiceFeature(self,i_account):
        req_data = json.dumps({'i_account':i_account})
        data = self.CallAPI(req_data, 'Account/get_service_features')
        return data                

    def GetCustomerInfo(self, account):
        req_data =  json.dumps({"id": account,"detailed_info": 0,})
        data = self.CallAPI(req_data, 'Account/get_account_info')
        return data

    def GetCustomerNameFromAccount(self, account):
        req_data =  json.dumps({"id": account,"detailed_info": 0})
        data = self.CallAPI(req_data, 'Account/get_account_info')
        dic = data['account_info']
        data = data['account_info'].get('customer_name',"")            
        return data

    def GetTrafficProfile(self, customer):
        req_data =  json.dumps({"i_customer": customer,"detailed_info": 0})
        data = self.CallAPI(req_data, 'Customer/get_customer_info')
        dic = data['customer_info']
        data = dic.get('i_traffic_profile',"")
        return data

    def GetTrafficProfileName(self, id):
        req_data = json.dumps({"i_traffic_profile" : id})
        data = self.CallAPI(req_data, 'TrafficProfile/get_traffic_profile_info')
        dic = data['traffic_profile_info']
        data = dic.get('name',"")
        return data

    def GetCustomerId(self, cname):
        customerinfo = {"name":cname,"detailed_info":0,}
        req_data = json.dumps(customerinfo)
        data = self.CallAPI(req_data, 'Customer/get_customer_info')
        dic = data.get('customer_info',"")
        if dic:
           data = dic.get('i_customer',"")
        else:
           data = 0
        return data

    def GetCustomField(self, pcustomerid):
        customerinfo = {"i_customer":pcustomerid}
        req_data = json.dumps(customerinfo)
        data = self.CallAPI(req_data, 'Customer/get_custom_fields_values')
        return data

    def GetCustomerList(self,offset="0",limit="500",i_customer_class="",name="", detailed_info=1):
        req_data = json.dumps({"i_customer_class":i_customer_class,"offset":offset,"limit":limit, "name":name, "detailed_info":detailed_info, "with_terminated":0, "bill_status":'O', "with_subresellers" :0,"get_total":1})
        data = self.CallAPI(req_data, 'Customer/get_customer_list')
        return data
   
    def GetTrafficProfileList(self, detailed=0):
        req_data = json.dumps({"with_extended_info" : detailed})
        data = self.CallAPI(req_data, 'TrafficProfile/get_traffic_profile_list')
        return data

    def GetCustomerClassList(self, reseller=0):
        req_data = json.dumps({"with_shared" : reseller})
        data = self.CallAPI(req_data, 'CustomerClass/get_customer_class_list')
        return data        

    def GetSessionList(self):
        req_data = json.dumps({"actual" : "Y"})
        data = self.CallAPI(req_data, 'BillingSession/get_active_sessions_list')
        return data                

    def GetCallList(self):
        req_data = json.dumps({"actual" : "Y"})
        data = self.CallAPI(req_data, 'BillingSession/get_active_calls_list')
        return data                
    
    def GetXDRSList(self,from_date, to_date, customer_id):
        req_data = json.dumps({ 'from_date':from_date,'to_date':to_date,'i_customer': customer_id, 'show_hidden':0})
        data = self.CallAPI(req_data, 'Customer/get_customer_xdrs')
        return data                

    def GetAccXDRSList(self,from_date, to_date, account_id):
        req_data = json.dumps({'from_date':from_date,'to_date':to_date,'i_account': account_id})
        data = self.CallAPI(req_data, 'Account/get_xdr_list')
        return data                

    def RevertXDRS(self, p_xdrsid,p_owner='account', p_comment=""):
        revert_list = [{"id":p_xdrsid, "owner":p_owner, "comment":p_comment, "hide":'Y'}]   
        req_data = json.dumps({"revert_list" : revert_list})
        data = self.CallAPI(req_data, 'CDR/revert_xdr_list')
        return data               

    def GetCustomerServiceFeatures(self,pcustomerid):
        req_data = json.dumps({'i_customer':pcustomerid})
        data = self.CallAPI(req_data, 'Customer/get_service_features')
        return data                

    def GetAccountsfromCustomer(self,pcustomerid):
        req_data = json.dumps({"i_customer":pcustomerid,"detailed_info":"1","limit":"1000","get_not_closed_accounts":"1","get_only_real_accounts":"1","get_total":"1"})
        data = self.CallAPI(req_data, 'Account/get_account_list',0)
        return data                

    def GetCustomersfromReseller(self, pparentid):
        req_data = json.dumps({"i_parent":pparentid,"detailed_info":"1","with_terminated":"0","limit":"1000"})
        data = self.CallAPI(req_data,'Customer/get_customer_list',0)
        return data                

    def GetServiceFeatures(self,prpconnectionid):
        req_data = json.dumps({'i_rp_connection': prpconnectionid})
        data = self.CallAPI(req_data, 'Customer/get_service_features')
        return data                

    def GetRoutePlanInfo(self,routeplan_id):
        req_data = json.dumps({'i_routing_plan': routeplan_id})
        data = self.CallAPI(req_data, 'RoutingPlan/get_routing_plan_info')
        return data                
        