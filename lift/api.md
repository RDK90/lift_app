# Lift App APIs

## Intro

These APIs are the endpoints to access the data from your training logs.

## APIs

### List all workouts

**Definition**

`GET /workouts`

**Response**
- `200 OK` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    },
    {
        "date": "26/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "T&G Bench",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "T&G Bench",
                "set": 2,
                "weight": 60,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
### Workouts by ID

**Definition**

`GET /workouts/{workout_id}`

**URL Parameters**

- `"workout_id":string` Date of workout in format (ddmmyyyy)

**Response**
- `200 OK` - on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
- `400 BAD REQUEST` - with invalid date format
```json
{
    "Error message": "Invalid date -9-99 found. Correct date format is DDMMYYY"
}
```
- `404 NOT FOUND` - with no training data found for given date
```json
{
    "Error message": "No workouts for date 2019-03-22 found"
}
```

**Definition**

`POST /workouts/{workout_id}`

**URL Parameters**

- `"workout_id":string` Date of workout in format (ddmmyy)

**Body Parameters**

- `"date":string` Date of workout
- `"tier":string` Tier of exercise (T1, T2, T3...etc)
- `"exercise":string` Name of exercise performed
- `"set":integer` Set number of the exercise
- `"repititions":integer` Number of repititions performed per set
- `"weight":float` Weight used for the exercise set
- `"repitition_category":string` Type of set (Warm up, work, AMRAP...etc)

If a workout is added with the same date as an existing entry, the previous workout will be overwritten

**Response**
- `201 Created` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
**Definition**

`PUT /workouts/{workout_id}`

**URL Parameters**

- `"workout_id":string` Date of workout in format (ddmmyy)

**Body Parameters**

- `"date":string` Date of workout
- `"tier":string` Tier of exercise (T1, T2, T3...etc)
- `"exercise":string` Name of exercise performed
- `"set":integer` Set number of the exercise
- `"repititions":integer` Number of repititions performed per set
- `"weight":float` Weight used for the exercise set
- `"repitition_category":string` Type of set (Warm up, work, AMRAP...etc)

**Response**
- `201 Created` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
**Definition**

`DELETE /workouts/{workout_id}`

**URL Parameters**

- `"workout_id":string` Date of workout in format (ddmmyy)

**Body Parameters**

No parameters

**Response**
- `204 No Content` on success

## Exercises by Name

**Definition**

`GET /exercises/{exercise_name}`

**URL Parameters** 

- `"exercise_name":string` Name of exercise

**Response**

- `200 OK` on success

```json
[
    {
        "exercise": "Low Bar Squat",
        "workout":[
            {
                "tier": "T1",
                "date": "23052019",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "date": "23052019",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]

```
**Definition**

`PUT /exercises/{exercise_name}`

**URL Parameters** 

- `"exercise_name":string` Name of exercise

**Response**

- `201 Created` on success

**Body Parameters**

- `"date":string` Date of workout
- `"tier":string` Tier of exercise (T1, T2, T3...etc)
- `"exercise":string` Name of exercise performed
- `"set":integer` Set number of the exercise
- `"repititions":integer` Number of repititions performed per set
- `"weight":float` Weight used for the exercise set
- `"repitition_category":string` Type of set (Warm up, work, AMRAP...etc)

```json
[
    {
        "exercise": "Low Bar Squat",
        "workout":[
            {
                "tier": "T1",
                "date": "23052019",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "date": "23052019",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]

```

### List all plans

**Definition**

`GET /plan`

**Response**
- `200 OK` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    },
    {
        "date": "26/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "T&G Bench",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "T&G Bench",
                "set": 2,
                "weight": 60,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
### Plans by Date

**Definition**

`GET /plans/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyyyy)

**Response**
- `200 OK` - on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
- `400 BAD REQUEST` - with invalid date format
```json
{
    "Error message": "Invalid date -9-99 found. Correct date format is DDMMYYY"
}
```
- `404 NOT FOUND` - with no training data found for given date
```json
{
    "Error message": "No workouts for date 2019-03-22 found"
}
```

**Definition**

`POST /plans/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyy)

**Body Parameters**

- `"date":string` Date of workout
- `"tier":string` Tier of exercise (T1, T2, T3...etc)
- `"exercise":string` Name of exercise performed
- `"set":integer` Set number of the exercise
- `"repititions":integer` Number of repititions performed per set
- `"weight":float` Weight used for the exercise set
- `"repitition_category":string` Type of set (Warm up, work, AMRAP...etc)

If a workout is added with the same date as an existing entry, the previous workout will be overwritten

**Response**
- `201 Created` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
**Definition**

`PUT /plans/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyy)

**Body Parameters**

- `"date":string` Date of workout
- `"tier":string` Tier of exercise (T1, T2, T3...etc)
- `"exercise":string` Name of exercise performed
- `"set":integer` Set number of the exercise
- `"repititions":integer` Number of repititions performed per set
- `"weight":float` Weight used for the exercise set
- `"repitition_category":string` Type of set (Warm up, work, AMRAP...etc)

**Response**
- `201 Created` on success

```json
[
    {
        "date": "25/03/19",
        "workout":[
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 1,
                "weight": 20,
                "repititions": 8,
                "repitition_category": "Warm up"
            },
            {
                "tier": "T1",
                "exercise": "Low Bar Squat",
                "set": 2,
                "weight": 70,
                "repititions": 4,
                "repitition_category": "Warm up"
            }
        ]
    }
]
```
**Definition**

`DELETE /plans/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyy)

**Body Parameters**

No parameters

**Response**
- `204 No Content` on success

### Characteristics by Date

**Definition**

`GET /characteristics/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyyyy)

**Response**
- `200 OK` - on success

```json
[
    {
            "date": "06092019",
            "week": 7,
            "time": "20:45",
            "toughness": 5,
            "awakeness": 5,
            "anxiety": 5,
            "soreness": 5,
            "enthusiasm": 5
        }
]
```
**Definition**

`POST /characteristics/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyyyy)

**Response**
- `201 CREATED` - on success

```json
[
    {
            "date": "06092019",
            "week": 7,
            "time": "20:45",
            "toughness": 5,
            "awakeness": 5,
            "anxiety": 5,
            "soreness": 5,
            "enthusiasm": 5
        }
]
```
- `400 BAD REQUEST` - with invalid date format
```json
{
    "Error message": "Invalid date -9-99 found. Correct date format is DDMMYYY"
}
```
- `406 NOT ACCEPTABLE` - with incorrect characteristic data found for given date
```json
{
    "Error Message": "Data is not valid"
}
```
**Definition**

`PUT /characteristics/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyyyy)

**Response**
- `201 CREATED` - on success

```json
[
    {
            "date": "06092019",
            "week": 7,
            "time": "20:45",
            "toughness": 5,
            "awakeness": 5,
            "anxiety": 5,
            "soreness": 5,
            "enthusiasm": 5
        }
]
```
- `400 BAD REQUEST` - with invalid date format
```json
{
    "Error message": "Invalid date -9-99 found. Correct date format is DDMMYYY"
}
```
- `406 NOT ACCEPTABLE` - with incorrect characteristic data found for given date
```json
{
    "Error Message": "Data is not valid"
}
```
**Definition**

`DELETE /characteristics/{date}`

**URL Parameters**

- `"date":string` Date of workout in format (ddmmyyyy)

**Response**
- `204 NO CONTENT` - on success

- `400 BAD REQUEST` - with invalid date format
```json
{
    "Error message": "Invalid date -9-99 found. Correct date format is DDMMYYY"
}
```