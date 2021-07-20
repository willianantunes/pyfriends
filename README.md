# PyFriends

This is WIP (Work In Progress). More to come soon! 😉

I'm using the compose service [app](https://github.com/willianantunes/pyfriends/blob/164423598fa12000079cea80eb87f070b44d7c2d/docker-compose.yaml#L4) as the remote interpreter.

## Delta architecture

I'm following the [Delta Architecture](https://databricks.com/blog/2019/08/14/productionizing-machine-learning-with-delta-lake.html) design pattern but I changed it a bit to fit this small project. So here you'll find the following layers:

- [Raw layer](./pyfriends/raw_layer): As the name suggests, you'll find the raw data without any processing. Although, in real projects, it may contain [profiling](https://en.wikipedia.org/wiki/Data_profiling) of all attributes, scoring the data in terms of its adherence to domain business and its typing, governance (like [data catalog](https://wiki.gccollab.ca/index.php?title=Data_Catalog&mobileaction=toggle_view_desktop) and many more), and security.
- [Integration layer](./pyfriends/integration_layer): The data is organized, and a clear pattern can be noticed. In other words, you can query the data through well-organized tables. They may have relationships that reflect how it is in the real world, but there are no KPIs created from it. It means the data is queryable and ready for insights but without business rules. As always, governance and security play a role here too.
- [Business layer](./pyfriends/business_layer): The KPIs can be found here, and it's a layer where a user without expertise in query can understand data easily. Again, governance and security are involved to guarantee many aspects of each domain.

## Tutorials I used to understand Pandas

- [jvns/pandas-cookbook](https://github.com/jvns/pandas-cookbook)
- [10 minutes to pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
- [Cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#cookbook)
- [Select using sub-query in Pandas](https://stackoverflow.com/a/59989971/3899136)
- [The Pandas DataFrame: Make Working With Data Delightful](https://realpython.com/pandas-dataframe/)
- [NEVER grow a DataFrame!](https://stackoverflow.com/a/56746204/3899136)
- [15 ways to create a Pandas DataFrame](https://towardsdatascience.com/15-ways-to-create-a-pandas-dataframe-754ecc082c17)
- [Python and Parquet Performance](https://blog.datasyndrome.com/python-and-parquet-performance-e71da65269ce)

Querying and plot:

- [Pandas GroupBy: Your Guide to Grouping Data in Python](https://realpython.com/pandas-groupby/)
- [Plot With Pandas: Python Data Visualization for Beginners](https://realpython.com/pandas-plot-python/)

## Credits

- [fangj](https://github.com/fangj/friends)
- [puneeth019/FRIENDS](https://github.com/puneeth019/FRIENDS)
- ["IT & Business: How to enable the true self-service, together" by William Porto](https://www.linkedin.com/pulse/ti-business-como-viabilizar-em-conjunto-o-verdadeiro-william-porto/)
