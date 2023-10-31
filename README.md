# MySuperDataCompany Inc. Data Upload and Query Engine

This project is a proof of concept for MySuperDataCompany Inc. It allows users to upload JSON and CSV files and subsequently query the data using a string named type, either through a web UI or a REST endpoint.

## Table of Contents
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Installation](#installation)
- [Usage](#usage)
  - [Web UI](#web-ui)
  - [REST Endpoint](#rest-endpoint)
- [Admin Panel](#admin-panel)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Web User Interface:**
  - File upload support for JSON and CSV.
  - File type control and raising error to the user.
  - Query with string interface to filter data from the uploaded file.
  - Nested JSON data is supported.

## Technical Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL (for storing meta data)
- **Data Querying:** pandasql

## Installation

1. Ensure you have Docker installed and running. If not the Official guides can be found at: [here](https://docs.docker.com/desktop/)
2. Clone this repository.
3. Navigate to the project folder
4. Use docker compose to set up and run the environment.
    `docker-compose up`

## Sample Files

You can find some sample files to test the application:

- [customers.json](samplefiles/customers.json)
- [customers.csv](samplefiles/customers.csv)

- ## Usage

### Web UI

1. Navigate to the web UI: [http://localhost:8000/data_app/upload/](http://localhost:8000/data_app/upload/)
2. Use the browse button to select either a JSON or CSV file from your local device.
3. Click the upload button.
4. After a successful upload, you'll be redirected to [http://localhost:8000/data_app/query/](http://localhost:8000/data_app/query/)
5. Enter your filtering string in the provided field.
6. Click 'Submit' and the query results will be displayed below in JSON format.

### REST Endpoint
To interact with the REST endpoint:

1. Make a **POST** request to the endpoint: [`http://localhost:8000/data_app/file-query/`](http://localhost:8000/data_app/file-query/).
2. Include the following parameters:
   - **file** (type: file): The file you want to upload.
   - **type** (type: string, optional): Any string you want to query the data with.
  
**Sample Request (using `curl`):**

curl --location --request POST 'http://localhost:8000/data_app/file-query/'
--form 'file=@<YOUR_FILE_PATH_HERE>/customers.json'
--form 'type=onur;'

Remember to replace `<YOUR_FILE_PATH_HERE>` with the actual path to your file.

### Admin Panel

The Admin Panel provides an interface to manage the contents of uploaded files.

- **URL**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Default Credentials**:
  - **Username**: `admin`
  - **Password**: `Data29102023`

#### Features:
- **Viewing Uploaded File Contents**: Navigate to the `uploaded data` section under `data_app` in the left pane to access all records from the latest uploaded table.

## Limitations

- File Type: Supports only JSON and CSV files.
- File Format: The system assumes a specific structure for the files. Proper formatting isn't checked rigorously.
- File Overwriting: Each time a new file is uploaded, it replaces the previously stored data. Consequently, users should be aware that prior upload contents are not preserved and will be permanently lost upon subsequent file submissions.
- File Size and Data Retrieval: The project was primarily developed as a proof of concept (POC) leveraging the Django Object Model. With this architectural choice:
  - There's a potential for substantial memory usage when dealing with large data sets.
  - Neither the web interface nor the user interface has pagination features. Therefore, client applications accessing these interfaces could experience performance issues or even failures if data retrieval operations return extensive data sets.

## Contributing

While this project is primarily a proof of concept, contributions are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

    
