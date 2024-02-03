"""
Firstly, I would try to cache as much of the Author Details as possible.
I would try to follow a strategy where I am able to track the "last_updated"
feature of each author (yes, it would take a complex database strategy which will
involve incorporating the feature update rules of different social media platforms:
For example: Facebook allows updating Display Name of user only once in 3 months.)

Given a larger number of API request quota, I would gather more pages at first, ideally
in units of 120. Then I would aggregate 120 items from ~ 4 content list API calls
and find out the unique authors there. For example, for page 1 in the Content List API,
We get 30 entries with 20 unique authors, so by only calling Author Detail API for the 20
unique authors, we have reduced the requirement for unnecessary API calls by 33%. For larger
aggregations, this will result in much less API calls.

Each API call is retried 4 times before sending Error response.

Aggregate statistics have been done "in-place" for each item to avoid multiple O(n) runtimes
that would occur due to using aggregate functions such as "sum" and would create large runtimes
for pages with large list size.



Debug turned false from .env file
"""
import os


from rest_framework.decorators import api_view
import requests
from django.http.response import JsonResponse


# URL and API KEY have been taken from .env file. This has been done to avoid using sensitive info inside code
midUrlTest = os.getenv("URL")
token = os.getenv("SECRET_KEY")

import time

@api_view(['GET'])
def get_content_list(request, page_no):
    print("inside content list")

    # query parameter validation added only to allow integers as page_no
    try:
        page_no = int(page_no)
    except Exception as e:
        return JsonResponse(status=400, data={"message":"Error. Invalid page no. Must be integer"})

    # Create header with token
    headers = {
        'x-api-key': f'{token}'
    }

    # Forward the request to the external API
    external_url = f"{midUrlTest}/contents?page={page_no}"
    response = requests.get(external_url, headers=headers, verify=False)


    # case for success
    if response.status_code == 200:
        # To avoid server downtime due to any kind of response error from URL
        try:
            data = response.json()
        except Exception as e:
            return JsonResponse(status=response.status_code, data={"message": "Error decoding JSON"})

        # Validating expected data structure for "data" key in response body
        if 'data' in data and isinstance(data['data'], list) and data['data'] != []:
            num_items = len(data['data'])
            items = data['data']

            # uncomment below line for small test cases
            # items = items[0:2]

            # find unique authors
            unique_author_ids = {item["author"]["id"] for item in items}
            unique_author_list = list(unique_author_ids)

            print(f"Number of items in 'data': {num_items}")
            print("unique_author_list: ", unique_author_list)
            print("unique_author_count: ", len(unique_author_list))

            # create empty dict with author id as key for storing each author details
            author_dict = {key: None for key in unique_author_list}
            print("author_dict : ", author_dict)

            for author_id in unique_author_list:

                # Just paranoia
                try:
                    author_id = int(author_id)
                except Exception as e:
                    return JsonResponse(status=400, data={"message": "Error. Invalid author id."})

                author_data = None
                # Attempting API call 4 times before failure
                for attempt in range(4):  # Retry up to 4 times
                    author_url = f"{midUrlTest}/authors/{author_id}"
                    author_url_response = requests.get(author_url, headers=headers, verify=False)

                    if author_url_response.status_code == 200:
                        author_data = author_url_response.json()
                        print("author_data['data']: ", author_data["data"])
                        break  # Break out of retry loop on success

                    # Wait for an exponentially increasing time before the next retry
                    time.sleep(2 ** attempt)

                # validate author data structure
                if author_data is not None and 'data' in author_data and isinstance(author_data['data'], list) and author_data['data'] != []:
                    author_dict[author_id] = author_data["data"]
                else:
                    # author_details key will contain string "Error Fetching Author Data" if somehow it fails to retrieve desired data
                    author_dict[author_id] = "Error Fetching Author Data"

            # Add 'author_data' to each item in 'data'
            for item in items:
                author_id = item["author"]["id"]

                # perform post statistics
                likes = item["stats"]["digg_counts"]["likes"]["count"]
                comments = item["stats"]["digg_counts"]["comments"]["count"]
                views = item["stats"]["digg_counts"]["views"]["count"]

                # add new stat metrics to each post
                item["stats"]["mean_engagement_per_user"] = ((likes + comments) / views) * 100
                item["stats"]["engagement_to_view_ratio"] = (likes + comments) / views
                item["author"]["author_data"] = author_dict[author_id]

        else:
            # content list api has returned empty "data" list
            return JsonResponse(status=404, data={"message": "Error: Data not found"})
    else:
        try:
            # if main server returns JSON error response, it will be forwarded to user
            data = response.json()
            return JsonResponse(status=response.status_code, data=data)
        except Exception as e:
            # the returned error response is not in JSON serializable format (for example: HTML Not Found page in APACHE, status code 500)
            return JsonResponse(status=response.status_code, data={"message": "Error: Failed Response"})

    return JsonResponse(status=200, data={"message" : "Success", "data": items})

# Function API Call with Aggregate Statistics
@api_view(['GET'])
def get_content_list_with_stat(request, page_no):
    print("inside stat")
    # query parameter validation added only to allow integers as page_no

    try:
        page_no = int(page_no)
    except Exception as e:
        return JsonResponse(status=400, data={"message": "Error. Invalid page no. Must be integer"})

    # Create header with token

    headers = {
        'x-api-key': f'{token}'
    }

    # Forward the request to the external API
    external_url = f"{midUrlTest}/contents?page={page_no}"
    response = requests.get(external_url, headers=headers, verify=False)

    if response.status_code == 200:
        try:
            data = response.json()
        except Exception as e:
            return JsonResponse(status=response.status_code, data={"message": "Error decoding JSON", "error": str(e)})
        # Validating expected data structure for "data" key in response body

        if 'data' in data and isinstance(data['data'], list) and data['data'] != []:
            num_items = len(data['data'])
            items = data['data']

            # uncomment below line for small test cases
            # items = items[0:2]

            # find unique authors
            unique_author_ids = {item["author"]["id"] for item in items}
            unique_author_list = list(unique_author_ids)

            print(f"Number of items in 'data': {num_items}")
            print("unique_author_list: ", unique_author_list)
            print("unique_author_count: ", len(unique_author_list))

            # create empty dict with author id as key for storing each author details
            author_dict = {key: None for key in unique_author_list}
            print("author_dict : ", author_dict)

            for author_id in unique_author_list:
                author_data = None
                # Attempting API call 4 times before failure
                for attempt in range(4):  # Retry up to 4 times
                    author_url = f"{midUrlTest}/authors/{author_id}"
                    author_url_response = requests.get(author_url, headers=headers, verify=False)

                    if author_url_response.status_code == 200:
                        author_data = author_url_response.json()
                        print("author_data['data']: ", author_data["data"])
                        break  # Break out of retry loop on success

                    # Wait for an exponentially increasing time before the next retry
                    time.sleep(2 ** attempt)

                # validate author data structure from response
                if author_data is not None and 'data' in author_data and isinstance(author_data['data'], list) and \
                        author_data['data'] != []:
                    author_dict[author_id] = author_data["data"]
                else:
                    # if for some reason server doesn't return desired data structure or returns empty list
                    author_dict[author_id] = "Error Fetching Author Data"

            # initialize dictionary for aggregate statistics with 0 values
            aggregate_stats = {
                "total_items": num_items,
                "total_likes": 0,
                "total_comments": 0,
                "total_views": 0,
                "mean_engagement_per_user": 0,
                "engagement_to_view_ratio": 0,
            }

            # Add 'author_data' to each item in 'data'
            for item in items:
                author_id = item["author"]["id"]
                likes = item["stats"]["digg_counts"]["likes"]["count"]
                comments = item["stats"]["digg_counts"]["comments"]["count"]
                views = item["stats"]["digg_counts"]["views"]["count"]

                # perform individual post statistics
                item["stats"]["mean_engagement_per_user"] = ((likes + comments) / views) * 100
                item["stats"]["engagement_to_view_ratio"] = (likes + comments) / views
                item["author"]["author_data"] = author_dict[author_id]

                # append values from post to aggregate statistics
                aggregate_stats["total_likes"] += likes
                aggregate_stats["total_comments"] += comments
                aggregate_stats["total_views"] += views

            # avoid 0 division error
            if aggregate_stats["total_views"] != 0:
                aggregate_stats["mean_engagement_per_user"] = (
                        (aggregate_stats["total_likes"] + aggregate_stats["total_comments"]) /
                        aggregate_stats["total_views"] * 100
                )
                aggregate_stats["engagement_to_view_ratio"] = (
                        aggregate_stats["total_likes"] + aggregate_stats["total_comments"] /
                        aggregate_stats["total_views"]
                )
        else:
            # if server returns empty post list
            return JsonResponse(status=404, data={"message": "Error: Data not found"})
    else:
        try:
            # parse server response as json and return message from server
            data = response.json()
            return JsonResponse(status=response.status_code, data=data)
        except Exception as e:
            # the returned error response is not in JSON serializable format (for example: HTML Not Found page in APACHE, status code 500)
            return JsonResponse(status=response.status_code, data={"message": "Error decoding JSON", "error": str(e)})

    return JsonResponse(status=200, data={"message": "Success", "data": items, "aggregate_stats": aggregate_stats})
