from app.tools.place_search import place_search


result = place_search.invoke({
    "location": "Varanasi",
    "query": "vegetarian restaurants near Kashi Vishwanath Temple"
})

print(result)