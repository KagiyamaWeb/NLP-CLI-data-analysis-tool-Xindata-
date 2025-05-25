import kagglehub
    
# Authenticate
kagglehub.login() # This will prompt you for your credentials.


path = kagglehub.dataset_download("shohinurpervezshohan/freelancer-earnings-and-job-trends", path="data/freelancer_earnings_bd.csv")