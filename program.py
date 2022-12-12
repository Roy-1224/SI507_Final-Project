import pandas as pd
import plotly.express as px
import json

class root:
    def __init__(self, zip_code):
        self.left = None
        self.right = None
        self.zipcode = zip_code
        self.id = []
    
    def insert(self, zip_code):
        if self.zipcode == zip_code:
            return
        elif zip_code < self.zipcode:
            if self.left:
                self.left.insert(zip_code)
            else:
                self.left = root(zip_code)
        else:
            if self.right:
                self.right.insert(zip_code)
            else:
                self.right = root(zip_code)

    def insert_id(self, zip_code, id):
        if self.zipcode == zip_code:
            self.id.append(id)
        elif self.zipcode > zip_code:
            self.left.insert_id(zip_code, id)
        else:
            self.right.insert_id(zip_code, id)

    def find(self, zip_code):
        if self.zipcode == zip_code:
            return self.id
        elif self.zipcode > zip_code and self.left != None:
            return self.left.find(zip_code)
        elif self.zipcode < zip_code and self.right != None:
            return self.right.find(zip_code)
        else:
            return []

    def to_dict(self):
        self_dict = {}
        id = [int(i) for i in self.id]
        zip = int(self.zipcode)
        self_dict[zip] = id
        if self.left != None:
            left = self.left.to_dict()
        else:
            left = None
        if self.right != None:
            right = self.right.to_dict()
        else:
            right = None
        self_dict['left'] = left
        self_dict['right'] = right
        return self_dict


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    bst = root(zip_code=data['zip_code'].values[0])
    for zip in data['zip_code'].unique():
        bst.insert(int(zip))
    for i in range(len(data)):
        id = data.loc[i, 'id']
        zip = data.loc[i, 'zip_code']
        bst.insert_id(zip_code=int(zip), id=id)
    zipcode = input("please enter your zip code: ")
    while zipcode.isdigit() == False:
        zipcode = input("Cannot identify your zipcode. Please enter again: ")
    while True:
        choice = input("Please enter 1 for general information of nearby restaurants, enter 2 to see a map of nearby restaurants, enter 3 to search for a category, enter exit to exit the program: ")
        # df = data[data['zip_code'] == int(zipcode)]
        id_list = bst.find(int(zipcode))
        df = data[data['id'].isin(id_list)]
        if choice == "1":
            df = df.sort_values(by='rating').head(min(len(df), 10))
            if len(df) != 0:
                print("The top", min(len(df), 10), "restaurants near your location are: ")
                print(df[['id', 'name', 'category', 'price', 'rating']].head(min(len(df), 10)))
            else:
                print("Cannot find restaurants near the given zip code.")
            zipcode = input("Please enter another zip code, or enter id of a restaurant to see detail information: ")
            while len(zipcode) < 5 or zipcode.isdigit() == False:
                # if len(zipcode) < 5 and len(df[df['id'] == int(zipcode)]) == 0:
                #     print("No nearby restaurant with such id.")
                if len(zipcode) < 5:
                    task2 = df[df['id'] == int(zipcode)]
                    if len(task2) != 0:
                        print("The information of restaurant whose id is", zipcode, "is listed below: ")
                        print(task2)
                    else:
                        print("No nearby restaurant with id", zipcode)
                zipcode = input("Please enter another zip code, or enter id of a restaurant to see detail information: ")
        elif choice == "2":
            fig = px.scatter_geo(df, lat='lat', lon='lng', hover_name="name", scope='usa', locationmode='USA-states')
            fig.update_geos(fitbounds="locations")
            fig.update_layout(title = 'USA Restaurant map', title_x=0.5)
            fig.show()
            zipcode = input("please enter another zip code: ")
            while zipcode.isdigit() == False:
                zipcode = input("Cannot identify your zipcode. Please enter again: ")
        elif choice == "3":
            category = input("Please enter the category you want to search: ").lower()
            while category.isdigit() == False:
                task3 = df[df['category'].str.lower().str.contains(category)]
                if len(task3) != 0:
                    print(task3)
                else:
                    print("Cannot find nearby restaurants with such category.")
                category = input("Please enter another zip code, or another category: ").lower()
                # if category.isdigit():
                #     zipcode = category
            zipcode = category
            # if len(task3) == 0:
            #     choice = input("Cannot find nearby restaurants with such category, please re-enter category or enter 1 for general information of nearby restaurants, enter 2 to see a map of nearby restaurants, enter 3 to search for a category: ")
            # else:
            #     print(task3)
            # if choice.isdigit() == False:
        elif choice.lower() == "exit":
            print("The program is ended, see you next time!")
            break
        else:
            # choice = input("Cannot parse your choice, please enter again: ")
            print("Cannot parse your choice.")
# json.