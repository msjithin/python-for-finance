import pandas as pd 

def get_social_security(country = 'France'):
    social_security_employee_df = pd.read_csv('social security for employees.csv')
    social_security_company_df = pd.read_csv('social security for companies.csv')
    ss_employee = social_security_employee_df[social_security_employee_df['Country'] == country]['Last']
    ss_company  = social_security_company_df[social_security_company_df['Country'] == country]['Last']
    return ss_employee.values[0] , ss_company.values[0]



if __name__ == '__main__':
    print( get_social_security()  )
