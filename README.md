
# Ambrosial: Swiggy Order History Analysis Package

Ambrosial is an Object-Oriented Programming (OOP) based installable Python package designed for comprehensive analysis of Swiggy order history data. This package offers a robust set of features for fetching, processing, and visualizing order data from the popular food delivery platform Swiggy.

## Features

- **Automated Data Retrieval**: Utilizes browser-cookies to fetch and update Swiggy order history automatically.
- **Data Preprocessing**: Handles data preprocessing, loading, caching, and conversion to DataClasses.
- **Comprehensive Analysis**: Generates analysis in both textual format and through various types of graphs.
- **Visualization Options**: Supports multiple graph types including Barplots, CalendarPlots, HeatMaps, Interactive Location HeatMaps, Word Clouds, Scatterplots, and Regression Lines.
- **High-Quality Code**: 100% type-annotated code with test coverage of more than 80%.

## Installation

```bash
git clone https://github.com/DistilledCode/ambrosial.git
cd ambrosial
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install .
```

### Additional Installation Options

#### Installing with development dependencies

If you want to contribute to the project or run tests, you can install the development dependencies:

```
pip install .[dev]
```

This will install additional packages for development, including pre-commit hooks, linters, and formatters.

#### Installing with test dependencies

To run the tests, you can install the test dependencies:

```
pip install .[test]
```

This will install pytest and any other testing-related packages.

### Verifying the Installation

After installation, you can verify that Ambrosial is correctly installed by running:

```
python -c "import ambrosial; print(ambrosial.__version__)"
```

This should print the version number of Ambrosial.

## Project Structure

```
src/
├── ambrosial/
│   ├── swan/
│   ├── swich/
│   └── swiggy/
```

## Basic Setup

> [!TIP]
> You can also refer to [advanced examples](./advanced/README.md)
>

To start using the package, import the necessary modules and create instances of the main classes:

```python
from ambrosial.swiggy import Swiggy
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

# Create instances
swiggy = Swiggy()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)
```

## Fetching and Loading Data

Before creating visualizations, you need to fetch or load your Swiggy order data:

```python
# Fetch new data (if you haven't already)
swiggy.fetch_orders()
swiggy.saveb()  # Save data for future use

# Or load previously saved data
swiggy.loadb()
```

## Creating Visualizations

Now you can use the `SwiggyChart` instance to create various visualizations:

### 1. Bar Plot

```python
# Create a bar plot of top 10 most ordered items
swich.barplot.restaurant_deltime()
```

![Bar Plot Example](https://github.com/DistilledCode/ambrosial/assets/107433905/b4e23f94-27d7-4411-933b-fbf2515682a6)

### 2. Calendar Plot

```python
# Create a calendar plot showing order frequency
swich.calplot.order_count()
```

![Calendar Plot Example](https://github.com/DistilledCode/ambrosial/assets/107433905/e08f6fe4-2ba8-4d90-8577-590456a69eba)

### 3. GitHub-style Contribution Map

```python
# Create a GitHub-style map of order history
swich.ghubmap.order_amount()
```

![GitHub-style Map Example](https://github.com/DistilledCode/ambrosial/assets/107433905/c811bbf9-c25d-4d75-90e1-0b6e5a561d98)

### 4. Heat Map

```python
# Create a heat map of order timings
swich.heatmap.order_count()
```

![Heat Map Example](https://github.com/DistilledCode/ambrosial/assets/107433905/7259dabf-3bb4-4bec-b611-ca6bfb0d5c37)

### 5. Interactive Location Map

```python
# Create an interactive map of order locations
swich.map.count_density()
```

![Interactive Map Example](https://github.com/DistilledCode/ambrosial/assets/107433905/66b127fa-ab33-44ed-8eb8-81a8fadc730e)

### 6. Regression Plot

```python
# Create a regression plot of order values over time
swich.regplot.ordamt_ordfee()
```

![Regression Plot Example](https://github.com/DistilledCode/ambrosial/assets/107433905/4b63017c-42ee-43c4-90aa-5d53be6022dc)

### 7. Word Cloud

```python
# Create a word cloud of restaurant names
swich.wcloud.restaurant_name()
```

![Word Cloud Example](https://github.com/DistilledCode/ambrosial/assets/107433905/d89326c8-52fd-4a8d-baa6-f0c43e590bb8)

## Customizing Visualizations

Many visualization methods allow for customization. For example:

```python
# Customize the bar plot
swich.barplot.top_items(
    top_n=15,
    title="Top 15 Most Ordered Items",
    color_palette="viridis"
)

# Customize the heat map
swich.heatmap.order_timings(
    cmap="YlOrRd",
    title="Order Timing Heatmap",
    figsize=(12, 8)
)
```

## Combining with Analytics

You can use the `SwiggyAnalytics` instance to get data for custom visualizations:

```python
# Get top restaurants data
top_restaurants = swan.restaurants.top_restaurants(top_n=5)

# Use this data to create a custom visualization
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(top_restaurants['name'], top_restaurants['order_count'])
plt.title("Top 5 Most Ordered From Restaurants")
plt.xlabel("Restaurant Name")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

## Saving Visualizations

Most visualization methods in the `SwiggyChart` class likely have options to save the generated plots. For example:

```python
swich.barplot.top_items(top_n=10, save_path="top_items.png")
swich.calplot.order_frequency(save_path="order_frequency.svg")
```

Remember to check the documentation or source code of each visualization method for specific parameters and options available.

## Example Visualizations

### Order Total vs. Order Fee Relationship

![Scatterplot Example 1](https://github.com/DistilledCode/ambrosial/assets/107433905/4b63017c-42ee-43c4-90aa-5d53be6022dc)

### Punctuality vs. Order Delivery Time

![Scatterplot Example 2](https://github.com/DistilledCode/ambrosial/assets/107433905/e7fa79c8-447c-4c20-94ee-5b647ddbc43e)

### Order Total vs. Order Fee Relationship

![Scatterplot Example 3](https://github.com/DistilledCode/ambrosial/assets/107433905/ac312710-2d05-419e-8765-049f0fbf9f85)

### Average Delivery Times for Various Restaurants

![Barplot Example 1](https://github.com/DistilledCode/ambrosial/assets/107433905/b4e23f94-27d7-4411-933b-fbf2515682a6)

### Average Amount Spent on Menu Items

![Barplot Example 2](https://github.com/DistilledCode/ambrosial/assets/107433905/bd21eb7b-848f-495d-9a9d-9c5431e326eb)

### Average Spending at Various Restaurants

![Barplot Example 3](https://github.com/DistilledCode/ambrosial/assets/107433905/ad16c8ba-2fb7-4835-8152-282036c9b51e)

### Weekly Order Count and Amount Heatmaps

![Heatmap Example 1](https://github.com/DistilledCode/ambrosial/assets/107433905/7259dabf-3bb4-4bec-b611-ca6bfb0d5c37)

![Heatmap Example 2](https://github.com/DistilledCode/ambrosial/assets/107433905/528e436c-02ce-4aa7-9583-7db6514cd4d3)

### Total Offer Availed Calendar for January 2022

![Heatmap Example 3](https://github.com/DistilledCode/ambrosial/assets/107433905/ed8433e8-5b96-49ee-9f36-3f52dcdcead4)

### Order Count, Discount, and Spending Trends (2021-2022)

![Calendar Plot - Total Order Count](https://github.com/DistilledCode/ambrosial/assets/107433905/c61cfb3c-9d51-4390-bb7b-9274f3fe1b1c)
![Calendar Plot - Total Discount](https://github.com/DistilledCode/ambrosial/assets/107433905/6f30bfa8-82d8-4072-b26c-146c9360038a)
![Calendar Plot - Total Amount Spent](https://github.com/DistilledCode/ambrosial/assets/107433905/c811bbf9-c25d-4d75-90e1-0b6e5a561d98)

### Monthly Amount Spent Heatmap Calendar View

![Calendar Plot - Total Amount Calculated](https://github.com/DistilledCode/ambrosial/assets/107433905/c5c6b52c-18d9-4dbf-8780-c679e42a8aa4)

### Monthly Order Count Heatmap Calendar View

![Calendar Plot - Order Count](https://github.com/DistilledCode/ambrosial/assets/107433905/e08f6fe4-2ba8-4d90-8577-590456a69eba)


### Cuisine Word Cloud

![Word Cloud - Restaurant Cuisine](https://github.com/DistilledCode/ambrosial/assets/107433905/5ca72936-a1b3-4e50-9ee5-513a15e0e950)

### Item Name Word Cloud

![Word Cloud - Item Names](https://github.com/DistilledCode/ambrosial/assets/107433905/740d0964-ab52-421f-a393-585aba678fd4)

### Restaurant Name Word Cloud

![Word Cloud - Restaurant Names](https://github.com/DistilledCode/ambrosial/assets/107433905/d89326c8-52fd-4a8d-baa6-f0c43e590bb8)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
