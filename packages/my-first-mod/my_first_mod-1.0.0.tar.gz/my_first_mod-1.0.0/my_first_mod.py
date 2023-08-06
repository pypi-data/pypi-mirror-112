def my_first(item_list,count):
    for each_movies in item_list:
            if isinstance(each_movies, list):
                    print("You are in the func"); my_first(each_movies,count)
            else:
                    print(each_movies, count); count = count+1