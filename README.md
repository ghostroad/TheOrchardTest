# The Orchard Code Test

This service, codenamed `Sietsema`[*](#footnote), manages and serves data extracted from 
[the NYC Department of Health & Mental Hygiene Restaurant Inspection Results Dataset](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j).

It's hosted at `https://sietsema.herokuapp.com`, and exposes an API that can be queried
using an http client like `curl` or Paw.

An example query using `curl` (see [below](#read-api) for an explanation):

```
curl "https://sietsema.herokuapp.com/search?min_grade=B&limit=5&cuisine=Thai&after=40799210"
```


## Installation

The service is written in Python 3 and requires a Postgres database. After cloning, perform the following steps to install it locally for development purposes:
- (Optionally) Create a virtual environment, using `conda` or `virtualenv`.
- Install the dependencies: ```pip install -r requirements.txt```.
- Export as environment variables: `FLASK_APP=sietsema.py` and `FLASK_ENV=development`.
- Create Postgres databases `sietsema` and `sietsema_test`.
- Migrate the development database: `flask db upgrade`.
- Start the server: `flask run`.
- Run tests: `pytest -v`.

Data can be imported into the service from a CSV file using `scripts/importer.py`. Running it provides usage information. As an example,
if I have the server running at `http://localhost:5000`, and a CSV file `DOHMH_New_York_City_Restaurant_Inspection_Results.csv`, containing data I'd like to import, I can do so by running

```
python importer.py -b http://localhost:5000 DOHMH_New_York_City_Restaurant_Inspection_Results.csv
```  

## Database structure

The service manages two types of entities: establishments and ratings. An establishment is identified by its "CAMIS", an ID 
assigned by the NYC DOHMH. Establishments are stored in the table `establishment`, which also holds information such as 
type of cuisine, address, and last inspection date.

A rating for an establishment is a grade of 'A', 'B', or 'C', assigned by an inspector. Ratings are stored in the table `rating`, 
along with the dates on which they were assigned. 

An establishment may have many ratings or none of them. Because our goal is to search for restaurants by rating, when we ingest data, we exclude records in the source that have a pending grade or that have no grade. 

Although we store all the grades a restaurant has received, when filtering restaurants by minimum grade, we do so on the basis of the *most recent* grade they have each received.

### Table structures

`establishment`:

| Field  | Type |
| ------------- | ------------- |
| `camis`  | integer (primary key)  |
| `dba`  | string (not null)  |
| `boro` | string |
| `building` | string |
| `street` | string |
| `zipcode` | string |
| `phone` | string |
| `cuisine` | string |
| `inspection_date` | date |

(Indices on `cuisine` and `camis`)

`rating`:

| Field  | Type |
| ------------- | ------------- |
| `id`  | serial (primary key)  |
| `grade`  | enum of 'A', 'B', or 'C' (not null)  |
| `date` | date (not null) |
| `camis` | integer (references `establishment.camis`) |

(Unique constraint on `(camis, date)` and indices on `id` and `(camis, date)`)


## Write API

### Create/Update Establishment

`PUT /establishments/<camis>` with a JSON request body of the form:

```
{
  "dba": "Pho Lien 2",
  "boro": "Manhattan",
  "building": "223",
  "street": "Canal Street",
  "zipcode": "10013",
  "phone": "2123456789",
  "cuisine": "Vietnamese",
  "inspection_date": "01/02/2019"
}
```

`dba` is required to be present and nonempty. All other fields are optional. If no entity with the supplied `camis` exists, one is 
created, otherwise the existing one is updated, as long as the `inspection_date` on the request is more recent than that on the 
existing entity.

Responses:
- `200` if all inputs are valid and the entity is updated/created.
- `403` if the inputs meet the requirements, but no update is performed to an existing entity because 
the information in the request is stale.
- `400` if the inputs are invalid.

### Create Rating

`POST /establishments/<camis>/ratings` with a JSON request body of the form:

```
{
  "grade": "B",
  "date": "03/02/2019"
}
```

Both fields are required. `grade` must be 'A', 'B', or 'C'. If a grade already exists for this establishment and this date,
nothing is modified on the server.

Responses:
- `200` if all inputs are valid and a rating has been created.
- `403` if inputs are valid, but a rating already exists for this date and establishment.
- `400` if the inputs are invalid.

## Read API

### Search for restaurants

`GET /search` with the following query parameters:
- `cuisine` (string, optional): filters the results by the specified cuisine
- `min_grade` (string, optional, defaults to 'B'): excludes establishments that do not have a rating, or that have a latest rating that 
is below the one specified.
- `after` (integer, optional): restricts to establishments that have a `camis` greater than this parameter, used for paginating through results.
- `limit` (integer, optional, defaults to 20): limits the number of entries returned.

*Note*: When determining whether an establishment satisfies the minimum grade requirement, we only look at its latest grade (although we store all the grades it has received).

#### Example

Request: `GET /search?cuisine=Polish&min_grade=B&limit=3&after=40561312`

Response:

```
[
  {
    "boro": "QUEENS",
    "building": "793",
    "camis": 40699061,
    "cuisine": "Polish",
    "dba": "I.O. CAFE",
    "latest_grade": "A",
    "latest_grade_date": "Tue, 26 Mar 2019 00:00:00 GMT",
    "phone": "7184561207",
    "street": "FAIRVIEW AVENUE",
    "zipcode": "11385"
  },
  {
    "boro": "BROOKLYN",
    "building": "694",
    "camis": 41057360,
    "cuisine": "Polish",
    "dba": "KROLEWSKIE JADLO",
    "latest_grade": "A",
    "latest_grade_date": "Wed, 13 Feb 2019 00:00:00 GMT",
    "phone": "7183838993",
    "street": "MANHATTAN AVENUE",
    "zipcode": "11222"
  },
  {
    "boro": "BROOKLYN",
    "building": "105",
    "camis": 41098752,
    "cuisine": "Polish",
    "dba": "LE FOND",
    "latest_grade": "A",
    "latest_grade_date": "Tue, 22 May 2018 00:00:00 GMT",
    "phone": "7183896859",
    "street": "NORMAN AVENUE",
    "zipcode": "11222"
  }
]
```

<a name="footnote">*</a> After the Village Voice food critic Robert Sietsema.
