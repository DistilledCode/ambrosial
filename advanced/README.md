## Table of Contents


1. Swiggy Class
   - Initialization
   - Fetching Orders
   - Saving and Loading Data
   - Retrieving Order Information
   - Retrieving Item Information
   - Retrieving Restaurant Information
   - Retrieving Address Information
   - Retrieving Offer Information
   - Retrieving Payment Information

2. AddressAnalytics
   - Visualizing Order Distribution Across Different Cities
   - Analyzing Delivery Time Trends Over Time
   - Analyzing Delivery Time Statistics Across Addresses
   - Visualizing Order Frequency on a Map

3. ItemAnalytics
   - Analyzing Item Popularity and Price Trends
   - Analyzing Item Categories and Their Performance
   - Analyzing Item Addons and Their Popularity
   - Analyzing Item Price Variations Over Time

4. OrderAnalytics
   - Analyzing Order Trends and Seasonality
   - Analyzing Delivery Time and Distance Trends
   - Analyzing Order Punctuality and Super Benefits
   - Analyzing Furthest Orders and Their Characteristics

5. SwiggyChart
   - barplot
   - calplot
   - heatmap
   - map
   - wcloud




## `Swiggy` class

The Swiggy class is the main interface for interacting with your Swiggy order data. It provides methods to fetch, process, and analyze your order history.

### Initialization

First, import and initialize the Swiggy class:

```python
from ambrosial.swiggy import Swiggy
from pathlib import Path

# Initialize with default settings
swiggy = Swiggy()

# Or, initialize with a custom path and detailed delivery address version
custom_path = Path("/path/to/your/data")
swiggy = Swiggy(path=custom_path, ddav=True)
```

### Fetching Orders

To fetch your order history from Swiggy's API:

```python
swiggy.fetch_orders()
print(f"Fetched {len(swiggy.orders_raw)} orders")
```

### Saving and Loading Data

After fetching, you can save the data for future use:

```python
# Save as JSON
swiggy.savej("my_orders.json")

# Save as MessagePack (more efficient)
swiggy.saveb("my_orders.msgpack")
```

To load previously saved data:

```python
# Load from JSON
swiggy.loadj("my_orders.json")

# Load from MessagePack
swiggy.loadb("my_orders.msgpack")
```

### Retrieving Order Information

#### Get a Specific Order

```python
order_id = 123456
order = swiggy.get_order(order_id)
print(f"Order {order_id}: {order.restaurant.name}, Total: {order.order_total}")
```

#### Get All Orders

```python
all_orders = swiggy.get_orders()
print(f"Total orders: {len(all_orders)}")
for order in all_orders[:5]:  # Print details of first 5 orders
    print(f"Order {order.order_id}: {order.restaurant.name}, Date: {order.order_time}")
```

### Retrieving Item Information

#### Get a Specific Item

```python
item_id = 789012
item = swiggy.get_item(item_id)
print(f"Item {item_id}: {item.name}, Price: {item.price}")
```

#### Get All Items

```python
all_items = swiggy.get_items()
print(f"Total unique items ordered: {len(all_items)}")
for item in all_items[:5]:  # Print details of first 5 items
    print(f"Item: {item.name}, Category: {item.category}")
```

### Retrieving Restaurant Information

#### Get a Specific Restaurant

```python
restaurant_id = 345678
restaurant = swiggy.get_restaurant(restaurant_id)
print(f"Restaurant {restaurant_id}: {restaurant.name}, Cuisine: {restaurant.cuisines}")
```

#### Get All Restaurants

```python
all_restaurants = swiggy.get_restaurants()
print(f"Total restaurants ordered from: {len(all_restaurants)}")
for restaurant in all_restaurants[:5]:  # Print details of first 5 restaurants
    print(f"Restaurant: {restaurant.name}, City: {restaurant.city}")
```

### Retrieving Address Information

#### Get a Specific Address

```python
address_id = 901234
address = swiggy.get_address(address_id)
print(f"Address {address_id}: {address.formatted_address}")

# If using detailed delivery address version (ddav=True)
address_version = 2
address = swiggy.get_address(address_id, ver=address_version)
```

#### Get All Addresses

```python
all_addresses = swiggy.get_addresses()
print(f"Total delivery addresses: {len(all_addresses)}")
for address in all_addresses[:5]:  # Print details of first 5 addresses
    print(f"Address: {address.formatted_address}")
```

### Retrieving Offer Information

#### Get Offers for a Specific Order

```python
order_id = 567890
offers = swiggy.get_offer(order_id)
for offer in offers:
    print(f"Offer applied on order {order_id}: {offer.description}, Discount: {offer.discount_amount}")
```

#### Get All Offers

```python
all_offers = swiggy.get_offers()
print(f"Total offers used: {len(all_offers)}")
for offer in all_offers[:5]:  # Print details of first 5 offers
    print(f"Offer: {offer.description}, Type: {offer.offer_type}")
```

### Retrieving Payment Information

#### Get Payment for a Specific Transaction

```python
transaction_id = 123456789
payments = swiggy.get_payment(transaction_id)
for payment in payments:
    print(f"Payment for transaction {transaction_id}: Method: {payment.payment_method}, Amount: {payment.amount}")
```

#### Get All Payments

```python
all_payments = swiggy.get_payments()
print(f"Total payments: {len(all_payments)}")
for payment in all_payments[:5]:  # Print details of first 5 payments
    print(f"Payment: Method: {payment.payment_method}, Type: {payment.payment_type}")
```

### Additional Information

- The `Swiggy` class uses a cache mechanism to optimize data retrieval. After the initial fetch or load, subsequent calls to get methods will be faster.
- The `ddav` parameter (detailed delivery address version) affects how address information is handled. When set to `True`, it allows for retrieving different versions of the same address.
- Error handling: Most methods will raise appropriate exceptions (e.g., `ValueError`, `KeyError`) if the requested data is not found or if there are issues with the input parameters.


## `AddressAnalytics`

### Example 1: Visualizing Order Distribution Across Different Cities

```python
import matplotlib.pyplot as plt
from collections import Counter

# Assuming swan is an instance of SwiggyAnalytics
address_analytics = swan.addresses

# Get grouped count of orders by city
city_order_count = address_analytics.grouped_count(group_by="city")

# Sort cities by order count
sorted_cities = sorted(city_order_count.items(), key=lambda x: x[1], reverse=True)
top_10_cities = dict(sorted_cities[:10])

# Create a pie chart
plt.figure(figsize=(12, 8))
plt.pie(top_10_cities.values(), labels=top_10_cities.keys(), autopct='%1.1f%%', startangle=90)
plt.title("Distribution of Orders Across Top 10 Cities")
plt.axis('equal')
plt.show()
```

### Example 2: Analyzing Delivery Time Trends Over Time

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get order history
order_history = address_analytics.order_history()

# Prepare data for plotting
data = []
for address, orders in order_history.items():
    for order in orders:
        data.append({
            'date': order.order_time.date(),
            'delivery_time': order.delivery_time / 60,  # Convert to minutes
            'address': address
        })

df = pd.DataFrame(data)

# Calculate moving average of delivery time
df['moving_avg'] = df.groupby('address')['delivery_time'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())

# Plot delivery time trends
plt.figure(figsize=(15, 10))
for address in df['address'].unique():
    address_data = df[df['address'] == address]
    plt.plot(address_data['date'], address_data['moving_avg'], label=address)

plt.title("Delivery Time Trends by Address")
plt.xlabel("Date")
plt.ylabel("Average Delivery Time (minutes)")
plt.legend(title="Address", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
```

### Example 3: Analyzing Delivery Time Statistics Across Addresses

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get delivery time statistics
delivery_stats = address_analytics.delivery_time_stats(unit="minute")

# Convert to DataFrame
stats_df = pd.DataFrame.from_dict(delivery_stats, orient='index')

# Create a heatmap of delivery time statistics
plt.figure(figsize=(12, 8))
sns.heatmap(stats_df, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Delivery Time Statistics Across Addresses")
plt.tight_layout()
plt.show()

# Create a box plot of delivery times
plt.figure(figsize=(15, 8))
sns.boxplot(data=stats_df, orient="h")
plt.title("Distribution of Delivery Times Across Addresses")
plt.xlabel("Delivery Time (minutes)")
plt.tight_layout()
plt.show()
```

### Example 4: Visualizing Order Frequency on a Map

```python
import folium
from folium.plugins import HeatMap

# Get coordinates of all orders
coordinates = address_analytics.coordinates()

# Create a map centered on the mean latitude and longitude
mean_lat = sum(coord.latitude for coord in coordinates) / len(coordinates)
mean_lon = sum(coord.longitude for coord in coordinates) / len(coordinates)

m = folium.Map(location=[mean_lat, mean_lon], zoom_start=10)

# Add a heatmap layer
heat_data = [[coord.latitude, coord.longitude] for coord in coordinates]
HeatMap(heat_data).add_to(m)

# Add markers for top 5 most frequent addresses
address_frequency = Counter(address_analytics.group())
top_5_addresses = address_frequency.most_common(5)

for address, frequency in top_5_addresses:
    folium.Marker(
        location=[address.latitude, address.longitude],
        popup=f"Address: {address.formatted_address}<br>Orders: {frequency}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Save the map
m.save("order_heatmap.html")
```
## `ItemAnalytics`


### Example 1: Analyzing Item Popularity and Price Trends

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Assuming swan is an instance of SwiggyAnalytics
item_analytics = swan.items

# Get grouped count of items
item_count = item_analytics.group()

# Get top 20 most ordered items
top_20_items = sorted(item_count.items(), key=lambda x: x[1], reverse=True)[:20]

# Create a DataFrame with item details
data = []
for item, count in top_20_items:
    summary = item_analytics.summarise(item.item_id)
    data.append({
        'name': item.name,
        'count': count,
        'avg_price': summary.avg_base_price,
        'avg_actual_cost': summary.avg_actual_cost,
        'discount_percentage': (summary.avg_base_price - summary.avg_actual_cost) / summary.avg_base_price * 100
    })

df = pd.DataFrame(data)

# Create a scatter plot of item popularity vs. price
plt.figure(figsize=(15, 10))
sns.scatterplot(data=df, x='avg_price', y='count', size='discount_percentage',
                hue='discount_percentage', sizes=(20, 500), palette='viridis')

for i, row in df.iterrows():
    plt.annotate(row['name'], (row['avg_price'], row['count']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.title('Item Popularity vs. Price')
plt.xlabel('Average Base Price')
plt.ylabel('Number of Orders')
plt.colorbar(label='Discount Percentage')
plt.tight_layout()
plt.show()
```

### Example 2: Analyzing Item Categories and Their Performance

```python
import matplotlib.pyplot as plt
import pandas as pd

# Get category details
category_details = item_analytics._get_category_details()

# Create a DataFrame
df = pd.DataFrame(category_details, columns=['category', 'count'])
df = df.sort_values('count', ascending=False).head(10)

# Create a stacked bar chart of top 10 categories
plt.figure(figsize=(15, 10))

bottom = 0
for index, row in df.iterrows():
    category = row['category']
    count = row['count']

    # Get items in this category
    items_in_category = item_analytics.grouped_instances('category', 'name')[category]

    # Get top 5 items in this category
    top_items = sorted(items_in_category, key=lambda x: item_analytics.group()[x], reverse=True)[:5]

    item_counts = [item_analytics.group()[item] for item in top_items]
    item_names = [item.name for item in top_items]

    plt.bar(category, item_counts, bottom=bottom, label=category)
    bottom += sum(item_counts)

    # Annotate with item names
    for i, count in enumerate(item_counts):
        plt.text(df.index.get_loc(index), bottom - count/2, item_names[i],
                 ha='center', va='center', rotation=90, fontsize=8)

plt.title('Top 10 Categories and Their Top 5 Items')
plt.xlabel('Category')
plt.ylabel('Number of Orders')
plt.legend(title='Categories', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### Example 3: Analyzing Item Addons and Their Popularity

```python
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

# Get addon details
addon_details = item_analytics._get_addons_detail()

# Create a DataFrame
df = pd.DataFrame(addon_details, columns=['addon', 'count'])
df = df.sort_values('count', ascending=False).head(20)

# Create a network graph of addons
G = nx.Graph()

for addon, count in df.iterrows():
    G.add_node(addon, size=count['count'])

# Add edges between addons that are often ordered together
for item in item_analytics.all_items:
    if item.addons:
        addons = [addon.name for addon in item.addons]
        for i in range(len(addons)):
            for j in range(i+1, len(addons)):
                if G.has_edge(addons[i], addons[j]):
                    G[addons[i]][addons[j]]['weight'] += 1
                else:
                    G.add_edge(addons[i], addons[j], weight=1)

# Draw the network
plt.figure(figsize=(20, 20))
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=[G.nodes[node]['size']*10 for node in G.nodes()],
                       node_color='lightblue', alpha=0.8)
nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight']/10 for u,v in G.edges()], alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title('Addon Popularity and Co-occurrence Network')
plt.axis('off')
plt.tight_layout()
plt.show()
```

### Example 4: Analyzing Item Price Variations Over Time

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Get top 5 most ordered items
top_items = sorted(item_analytics.group().items(), key=lambda x: x[1], reverse=True)[:5]

# Prepare data for plotting
data = []
for item, _ in top_items:
    orders = item_analytics.associated_orders(item.item_id)
    for order in orders:
        for order_item in order.items:
            if order_item.item_id == item.item_id:
                data.append({
                    'item_name': item.name,
                    'order_date': order.order_time.date(),
                    'price': order_item.price,
                    'actual_cost': order_item.total_actual_cost
                })

df = pd.DataFrame(data)

# Plot price variations over time
plt.figure(figsize=(15, 10))
for item_name in df['item_name'].unique():
    item_data = df[df['item_name'] == item_name]
    sns.lineplot(data=item_data, x='order_date', y='price', label=f"{item_name} (Base Price)")
    sns.lineplot(data=item_data, x='order_date', y='actual_cost', label=f"{item_name} (Actual Cost)", linestyle='--')

plt.title('Price Variations of Top 5 Items Over Time')
plt.xlabel('Order Date')
plt.ylabel('Price')
plt.legend(title='Items', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```
## `OrderAnalytics`


### Example 1: Analyzing Order Trends and Seasonality

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Assuming swan is an instance of SwiggyAnalytics
order_analytics = swan.orders

# Get monthly order counts and amounts
monthly_counts = order_analytics.tseries_count(bins="year+month_")
monthly_amounts = order_analytics.tseries_amount(bins="year+month_")

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime([f"{k[:4]}-{k[5:7]}-01" for k in monthly_counts.keys()]),
    'count': monthly_counts.values(),
    'amount': monthly_amounts.values()
})
df.set_index('date', inplace=True)

# Perform time series decomposition
decomposition_count = seasonal_decompose(df['count'], model='additive', period=12)
decomposition_amount = seasonal_decompose(df['amount'], model='additive', period=12)

# Plot the results
fig, axs = plt.subplots(4, 2, figsize=(20, 30))

# Order Count
axs[0, 0].plot(df.index, df['count'])
axs[0, 0].set_title('Original Order Count')
axs[1, 0].plot(decomposition_count.trend)
axs[1, 0].set_title('Trend')
axs[2, 0].plot(decomposition_count.seasonal)
axs[2, 0].set_title('Seasonality')
axs[3, 0].plot(decomposition_count.resid)
axs[3, 0].set_title('Residuals')

# Order Amount
axs[0, 1].plot(df.index, df['amount'])
axs[0, 1].set_title('Original Order Amount')
axs[1, 1].plot(decomposition_amount.trend)
axs[1, 1].set_title('Trend')
axs[2, 1].plot(decomposition_amount.seasonal)
axs[2, 1].set_title('Seasonality')
axs[3, 1].plot(decomposition_amount.resid)
axs[3, 1].set_title('Residuals')

plt.tight_layout()
plt.show()
```

### Example 2: Analyzing Delivery Time and Distance Trends

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Get weekly delivery time and distance statistics
weekly_del_time = order_analytics.tseries_del_time(bins="week_")
weekly_distance = order_analytics.tseries_distance(bins="week_")

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime([f"{k[:4]}-W{k[5:7]}-1" for k in weekly_del_time.keys()]),
    'avg_del_time': [d.mean for d in weekly_del_time.values()],
    'avg_distance': [d.mean for d in weekly_distance.values()]
})

# Calculate moving averages
df['del_time_ma'] = df['avg_del_time'].rolling(window=4).mean()
df['distance_ma'] = df['avg_distance'].rolling(window=4).mean()

# Create the plot
fig, ax1 = plt.subplots(figsize=(15, 8))

ax1.set_xlabel('Date')
ax1.set_ylabel('Average Delivery Time (minutes)', color='tab:blue')
ax1.plot(df['date'], df['avg_del_time'], color='tab:blue', alpha=0.3)
ax1.plot(df['date'], df['del_time_ma'], color='tab:blue', label='Delivery Time (4-week MA)')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Average Distance (km)', color='tab:orange')
ax2.plot(df['date'], df['avg_distance'], color='tab:orange', alpha=0.3)
ax2.plot(df['date'], df['distance_ma'], color='tab:orange', label='Distance (4-week MA)')
ax2.tick_params(axis='y', labelcolor='tab:orange')

fig.tight_layout()
plt.title('Weekly Average Delivery Time and Distance Trends')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 1), bbox_transform=ax1.transAxes)
plt.show()
```

### Example 3: Analyzing Order Punctuality and Super Benefits

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Get monthly punctuality and super benefits statistics
monthly_punctuality = order_analytics.tseries_punctuality(bins="year+month_")
monthly_benefits = order_analytics.tseries_super_benefits(bins="year+month_")

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime([f"{k[:4]}-{k[5:7]}-01" for k in monthly_punctuality.keys()]),
    'on_time': [p.on_time for p in monthly_punctuality.values()],
    'late': [p.late for p in monthly_punctuality.values()],
    'early': [p.early for p in monthly_punctuality.values()],
    'benefits_amount': [b.amount for b in monthly_benefits.values()],
    'benefits_count': [b.count for b in monthly_benefits.values()]
})

# Calculate punctuality percentages
df['total_orders'] = df['on_time'] + df['late'] + df['early']
df['on_time_pct'] = df['on_time'] / df['total_orders'] * 100
df['late_pct'] = df['late'] / df['total_orders'] * 100
df['early_pct'] = df['early'] / df['total_orders'] * 100

# Create the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 15))

# Punctuality plot
ax1.stackplot(df['date'], df['on_time_pct'], df['late_pct'], df['early_pct'],
              labels=['On Time', 'Late', 'Early'], alpha=0.7)
ax1.set_ylabel('Percentage of Orders')
ax1.set_title('Monthly Order Punctuality')
ax1.legend(loc='upper left')

# Super Benefits plot
ax2.bar(df['date'], df['benefits_amount'], alpha=0.7, label='Benefits Amount')
ax2.set_xlabel('Date')
ax2.set_ylabel('Benefits Amount', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

ax3 = ax2.twinx()
ax3.plot(df['date'], df['benefits_count'], color='tab:orange', label='Benefits Count')
ax3.set_ylabel('Benefits Count', color='tab:orange')
ax3.tick_params(axis='y', labelcolor='tab:orange')

ax2.set_title('Monthly Super Benefits')
fig.legend(loc='upper right', bbox_to_anchor=(1, 0.95))

plt.tight_layout()
plt.show()
```

### Example 4: Analyzing Furthest Orders and Their Characteristics

```python
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Get weekly furthest order details
weekly_furthest = order_analytics.tseries_furthest_order(bins="week_")

# Create a DataFrame
df = pd.DataFrame({
    'date': pd.to_datetime([f"{k[:4]}-W{k[5:7]}-1" for k in weekly_furthest.keys()]),
    'distance': [f.distance for f in weekly_furthest.values()],
    'delivery_time': [f.delivery_time for f in weekly_furthest.values()],
    'amount': [f.amount for f in weekly_furthest.values()],
    'restaurant': [f.restaurant_name for f in weekly_furthest.values()]
})

# Create the plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 20))

# Distance plot
sns.scatterplot(data=df, x='date', y='distance', size='amount', hue='restaurant', ax=ax1)
ax1.set_title('Weekly Furthest Order Distance')
ax1.set_ylabel('Distance (km)')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Delivery Time plot
sns.scatterplot(data=df, x='date', y='delivery_time', size='amount', hue='restaurant', ax=ax2)
ax2.set_title('Weekly Furthest Order Delivery Time')
ax2.set_ylabel('Delivery Time (minutes)')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Amount plot
sns.scatterplot(data=df, x='date', y='amount', size='distance', hue='restaurant', ax=ax3)
ax3.set_title('Weekly Furthest Order Amount')
ax3.set_ylabel('Order Amount')
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# Additional analysis: Top 5 restaurants for furthest orders
top_restaurants = df['restaurant'].value_counts().head()
print("Top 5 Restaurants for Furthest Orders:")
print(top_restaurants)
```
## `SwiggyChart.barplot`

### 1. Average Delivery Time by Restaurant:

```python
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

swan = SwiggyAnalytics()
swich = SwiggyChart(swan)

swich.barplot.restaurant_deltime(threshold=5, gtype="average")
```

This will create a bar plot showing the average delivery time for restaurants with at least 5 orders.

### 2. Total Spending on Items:

```python
swich.barplot.item_spending(threshold=3, gtype="total")
```

This generates a bar plot displaying the total amount spent on items that have been ordered at least 3 times.

### 3. Order Count by Restaurant:

```python
swich.barplot.restaurant_count(threshold=4)
```

This creates a bar plot showing the number of orders from each restaurant, including only those with at least 4 orders.

### 4. Coupon Discount Analysis:

```python
swich.barplot.coupon_discount(threshold=2, gtype="average")
```

This produces a bar plot illustrating the average discount amount for coupons used at least twice.

### 5. Payment Method Analysis:

```python
swich.barplot.payment_method(gtype="total")
```

This generates a bar plot showing the total transaction amount for each payment method.

### 6. Item Order Count:

```python
swich.barplot.item_count(threshold=5)
```

This creates a bar plot displaying the number of times each item has been ordered, including only items ordered at least 5 times.

### 7. Restaurant Spending Analysis:

```python
swich.barplot.restaurant_spending(threshold=3, gtype="average")
```

This produces a bar plot showing the average amount spent per order at each restaurant, including only restaurants with at least 3 orders.

### 8. Payment Type Analysis:

```python
swich.barplot.payment_type(gtype="average")
```

This generates a bar plot illustrating the average transaction amount for each payment type.

For all these examples, you can add additional customization using kwargs:

```python
swich.barplot.restaurant_deltime(
    threshold=5,
    gtype="average",
    title="Average Delivery Time by Restaurant",
    xlabel="Restaurant",
    ylabel="Delivery Time (minutes)",
    figsize=(12, 6),
    color="skyblue"
)
```


## `SwiggyChart.calplot`


### 1. Calendar Plot of Total Order Amount:

```python
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

swan = SwiggyAnalytics()
swich = SwiggyChart(swan)

swich.calplot.cal_order_amount()
```

This will create a calendar plot showing the total order amount for each day across all years.

### 2. Calendar Plot of Order Count:

```python
swich.calplot.cal_order_count()
```

This generates a calendar plot displaying the number of orders placed each day across all years.

### 3. Calendar Plot of Offer Amount Availed:

```python
swich.calplot.cal_offer_amount()
```

This creates a calendar plot showing the total offer amount availed each day across all years.

### 4. Monthly Plot of Order Amount:

```python
swich.calplot.month_order_amount(month=7, year=2023)
```

This produces a monthly plot illustrating the total order amount for each day in July 2023.

### 5. Monthly Plot of Order Count:

```python
swich.calplot.month_order_count(month=12, year=2022)
```

This generates a monthly plot showing the number of orders placed each day in December 2022.

### 6. Monthly Plot of Offer Amount:

```python
swich.calplot.month_offer_amount(month=3, year=2024)
```

This creates a monthly plot displaying the total offer amount availed each day in March 2024.

You can add additional customization using kwargs for all these methods:

```python
swich.calplot.cal_order_amount(
    title="Total Order Amount by Day",
    cmap="YlOrRd",
    figsize=(16, 10),
    dpi=300
)
```

This will create a customized calendar plot with a specific title, color map, figure size, and resolution.

For monthly plots, you can add similar customizations:

```python
swich.calplot.month_order_count(
    month=5,
    year=2023,
    title="Order Count for May 2023",
    cmap="viridis",
    figsize=(12, 8)
)
```

## `SwiggyChart.heatmap`


### 1. Heatmap of Total Order Amount:

```python
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

swan = SwiggyAnalytics()
swich = SwiggyChart(swan)

swich.heatmap.order_amount(bins="month_+week_")
```

This will create a heatmap showing the total order amount for each week of each month.

### 2. Heatmap of Order Count:

```python
swich.heatmap.order_count(bins="month_+day")
```

This generates a heatmap displaying the number of orders for each day of each month.

### 3. Heatmap of Average Delivery Time:

```python
swich.heatmap.avg_delivery_time(bins="month_+day")
```

This creates a heatmap showing the average delivery time for each day of each month.

### 4. Heatmap of Offer Discount:

```python
swich.heatmap.offer_discount(bins="month_+week_")
```

This produces a heatmap illustrating the total offer discount availed for each week of each month.

### 5. Heatmap of Super Benefits:

```python
swich.heatmap.super_benefits(bins="month_+day")
```

This generates a heatmap showing the total super benefits availed for each day of each month.

### 6. Heatmap of Total Savings:

```python
swich.heatmap.total_saving(bins="month_+week_")
```

This creates a heatmap displaying the total savings (discount + super benefits) for each week of each month.

You can add additional customization using kwargs for all these methods:

```python
swich.heatmap.order_amount(
    bins="month_+week_",
    drop_empty=False,
    cmap="YlOrRd",
    figsize=(16, 10),
    annot=True,
    fmt=".0f"
)
```

This will create a customized heatmap with a specific color map, figure size, annotations, and number format. It will also include empty cells (drop_empty=False).

You can also change the binning to get different perspectives:

```python
swich.heatmap.order_count(bins="year_+month_")
```

This will show the order count for each month of each year.

Remember to import matplotlib.pyplot and call plt.show() after creating the plot if you're not in an interactive environment:

```python
import matplotlib.pyplot as plt

swich.heatmap.avg_delivery_time(bins="month_+day")
plt.show()
```

## `SwiggyChart.map`

Certainly! Here are simple examples demonstrating the use of the `SwiggyChart.Map` class:

### 1. Create a density map based on order count for a specific city:

```python
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

swan = SwiggyAnalytics()
swich = SwiggyChart(swan)

# Create a density map for Bangalore
bangalore_map = swich.map.count_density(city="Bangalore")
```

This will create an interactive map showing the density of orders in Bangalore.

### 2. Create a nationwide density map based on order amount:

```python
# Create a nationwide map based on order amount
india_map = swich.map.amount_density(nationwide=True)
```

This generates an interactive map of India showing the density of order amounts across different locations.

### 3. Create a custom map with specific hover and popup formats:

```python
# Custom hover and popup formats
hover_format = "{restaurant_name}: {order_count} orders"
popup_format = """
<b>{restaurant_name}</b><br>
Orders: {order_count}<br>
Total Amount: ₹{total_amount:.2f}<br>
Average Order Value: ₹{avg_order_value:.2f}
"""

mumbai_map = swich.map.count_density(
    city="Mumbai",
    hover_frmt=hover_format,
    popup_frmt=popup_format
)
```

This creates a map of Mumbai with custom hover and popup information for each marker.

### 4. Create a map without saving it to a file:

```python
# Create a map without saving
delhi_map = swich.map.amount_density(city="Delhi", save=False)
```

This generates a map for Delhi based on order amounts but doesn't save it as an HTML file.

### 5. Display the map in a Jupyter notebook:

```python
# Assuming you're in a Jupyter notebook
from IPython.display import display

hyderabad_map = swich.map.count_density(city="Hyderabad")
display(hyderabad_map)
```

This will display the interactive map directly in the Jupyter notebook.

### 6. Combine nationwide and city-specific maps:

```python
# Create both nationwide and city-specific maps
india_map = swich.map.count_density(nationwide=True)
chennai_map = swich.map.count_density(city="Chennai")

# Display both maps in a Jupyter notebook
display(india_map)
display(chennai_map)
```
## `SwiggyChart.wcloud`


### 1. Create a word cloud for item categories:

```python
from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart

swan = SwiggyAnalytics()
swich = SwiggyChart(swan)

# Create a word cloud for item categories
swich.wcloud.item_category()
```

This will create a word cloud image of item categories and save it as "item_category.png" in the default path.

### 2. Create a word cloud for item names with custom parameters:

```python
swich.wcloud.item_name(
    fname="my_favorite_items.png",
    icon_name="fas fa-utensils",
    background_color="white",
    gradient="horizontal",
    colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
)
```

This generates a word cloud of item names with a custom filename, icon, background color, gradient, and color scheme.

### 3. Create a word cloud for restaurant cuisines:

```python
swich.wcloud.restaurant_cuisine(freq_weight=True)
```

This creates a word cloud of restaurant cuisines, with the size of each word weighted by its frequency.

### 4. Create a word cloud for restaurant names with a custom path:

```python
from pathlib import Path

custom_path = Path("/path/to/your/directory")
swich.wcloud.restaurant_name(path=custom_path, fname="favorite_restaurants.png")
```

This generates a word cloud of restaurant names and saves it in a custom directory.

### 5. Create a word cloud for coupon codes:

```python
swich.wcloud.coupon_code(
    icon_name="fas fa-tag",
    background_color="#F0F0F0",
    max_font_size=100,
    min_font_size=10
)
```

This creates a word cloud of coupon codes with a custom icon, background color, and font size range.

### 6. Create multiple word clouds with different styles:

```python
# Item categories with a circular shape
swich.wcloud.item_category(icon_name="fas fa-circle", shape="circle")

# Item names with a custom font
swich.wcloud.item_name(font_path="/path/to/your/custom/font.ttf")

# Restaurant cuisines with a mask image
swich.wcloud.restaurant_cuisine(mask="/path/to/your/mask_image.png")
```

These examples create word clouds with different shapes, fonts, and mask images.

Remember that the word cloud images will be saved as PNG files in the specified or default directory. You can open these images to view the word clouds.

To display the word cloud in a Jupyter notebook immediately after creation, you can use:

```python
from IPython.display import Image, display

swich.wcloud.restaurant_name()
display(Image("restaurant_name.png"))
```
