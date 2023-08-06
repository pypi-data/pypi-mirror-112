### Project Structure for MLflow integrated ML Projects

This cli tool generates the following directory structure for quickstart ML projects

installaton:  

    pip install aihubcli

example use:  
    
    aihubcli create mytestproject
    

It generates the project with following structure

    Project
    |
    +--- Input
    |    |
    |    +--- raw               Raw data here
    |    |
    |    +--- interim           Any intermediate data, to pause and continue experiments
    |    |
    |    +--- processed         Processed data ready for ML pipeline
    |
    +--- output
    |    |
    |    +--- models             Model pickle or model weights stored here
    |    |
    |    +--- artifacts         Serialized artifacts like LabelEncoder, Vectorizer etc
    |    |
    |    +--- images            All plots and visualizations goes here
    |    |
    |    +--- Results           If the results needs to be stored for review, save here
    |
    +--- notebooks              All notebooks and experiments resides here
    |
    +--- src                    Final program, with training and prediction pipeline
    |
    |
    README.md                   Description and instruction about the project
    MLProject                   MLflow project file. If you want to use this directory as MLflow project
    Requirements.txt            python dependencies
    Config.yml                  configuration key values in yaml format
 
