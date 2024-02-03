# Project Name: Zelf Hackathon 1.0

## Project Overview

This project is a Django web application with API endpoints providing content and author details along with aggregated statistics. The API responses include information about individual content items as well as overall statistics.

## Environment Setup

- **Python Version:** 3.10
- **Install Requirements:**
  ```
  pip install -r requirements.txt
  ```

## How to Run

To run the Django development server, use the following command:
```
python zelf_hackathon_1.0/myproject_original/manage.py runserver
```

## API Documentations

### 1. Get Content List with Author Details

- **URL:** `<django_app_url>/api/content/pages/<page_no>`
- **Request Type:** GET

#### Sample Response for Single Item List:

```json
{
  "message": "Success",
  "data": [
    {
      "unique_id": 1996096,
      "unique_uuid": "31fca27a-9d67-458d-8e60-5be49a7933db",
      "origin_unique_id": "CqiKhfMA0iu",
      "creation_info": {
        "created_at": "2023-05-12T13:41:53.019333Z",
        "timestamp": "2023-05-12T13:41:53.019333Z"
      },
      "author": {
        "id": 919301,
        "username": "stuffedddd",
        "author_data": [
          {
            "unique_id": 919301,
            "unique_uuid": "ig_stuffedddd",
            "origin_unique_id": "ig_stuffedddd",
            // ... additional author data
          }
        ]
      },
      "stats": {
        "digg_counts": {
          "likes": {
            "id": 2992,
            "count": 119778
          },
          "views": {
            "id": 2885,
            "count": 2600000
          },
          "comments": {
            "id": 2293,
            "count": 199
          }
        },
        "mean_engagement_per_user": 4.6145,
        "engagement_to_view_ratio": 0.046145
      }
      // ... additional content data
    }
    // ... additional content items
  ]
}
```

### 2. Get Content List with Author Details and Aggregated Statistics

- **URL:** `<django_app_url>/api/content/pages/<page_no>/stat`
- **Request Type:** GET

#### Sample Response for Single Item List:

```json
{
  "message": "Success",
  "data": [
    {
      "unique_id": 1996096,
      "unique_uuid": "31fca27a-9d67-458d-8e60-5be49a7933db",
      "origin_unique_id": "CqiKhfMA0iu",
      "creation_info": {
        "created_at": "2023-05-12T13:41:53.019333Z",
        "timestamp": "2023-05-12T13:41:53.019333Z"
      },
      "author": {
        "id": 919301,
        "username": "stuffedddd",
        "author_data": [
          {
            "unique_id": 919301,
            "unique_uuid": "ig_stuffedddd",
            "origin_unique_id": "ig_stuffedddd",
            // ... additional author data
          }
        ]
      },
      "stats": {
        "digg_counts": {
          "likes": {
            "id": 2992,
            "count": 119778
          },
          "views": {
            "id": 2885,
            "count": 2600000
          },
          "comments": {
            "id": 2293,
            "count": 199
          }
        },
        "mean_engagement_per_user": 4.6145,
        "engagement_to_view_ratio": 0.046145
      }
      // ... additional content data
    }
    // ... additional content items
  ],
  "aggregate_stats": {
    "total_items": 30,
    "total_likes": 135078,
    "total_comments": 258,
    "total_views": 14700000,
    "mean_engagement_per_user": 0.9206530612244899,
    "engagement_to_view_ratio": 135078.000017551
  }
}
```

Feel free to reach out if you have any questions or need further assistance.
