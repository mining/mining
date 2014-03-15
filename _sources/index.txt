
Open Mining - Business Intelligence (BI) Application Server
==========================================================

.. image:: https://raw.github.com/avelino/mining/master/assets/image/openmining.io.png
   :name: logo

.. sidebar:: Links

 - `Bug tracker <http://github.com/avelino/mining/issues>`_
 - IRC: (`#openmining <http://webchat.freenode.net?channels=openmining>`_) on Freenode
 - `Downloads <http://pypi.python.org/pypi/mining/>`_
 - `Source code <https://github.com/avelino/mining>`_


Why Open Mining?
----------------

**Open Mining** is software for creating OLAP (online analytical processing) cubes (multi-dimensional) using Numpy, 
Scipy and Pandas for data management and flexibility in processing dynamical filters. Open-source provider of 
reporting, analysis, dashboard, data mining and workflow capabilities.


Cube, Dimensions, Facts and Measures
------------------------------------

The application models the data as a cube with multiple dimensions:

.. figure:: _static/cubes-slice_and_dice-cell.png
    :align: center
    :width: 400px

The most detailed unit of the data is a *fact*. Fact can be a contract,
invoice, spending, task, etc. Each fact might have a *measure* â€“ an attribute
that can be measured, such as: price, amount, revenue, duration, tax,
discount, etc.

The *dimension* provides context for facts. Is used to:

* filter queries or reporst
* controls scope of aggregation of facts
* group by fields
* used for ordering or sorting
* defines master-detail relationship

Dimension can have multiple *hierarchies*, for example the date dimension
might have year, month and day levels in a hierarchy.


Reporting features
------------------

Which reporting solution is the best? Which tool to choose? 
These are the question that all companies' managers need to answer in the beginning of firm's existence. 
Although the choice always depends on customer, there are more and less meaningful features that might 
influence on the evaluation. Checking and comparing the most important ones is necessary for distinguishing 
worth-interesting solutions from inappropriate ones. 
In the case of **Open Mining, crucial features are good enough not to denounce that we're considering a free, 
open source software**.


* The advancement of **reporting algorithm** is probably the strongest side of Open Mining. Complex 
  system is prepared well enough to support all types of reports regardless of their destination, input data, 
  and output format.
* The ideal situation would be if every department of an enterprise were using one common reporting solution. 
  Unfortunately, it's rather a rare situation, a possibility for reading reports from all of them is therefore 
  very useful. And that's what Open Mining offers. **Multiple data sources available** help also with migrating 
  data if the company thinks about replacing former solutions with one for all. Among many others, these are
  the most common data sources operable with Open Mining solutions: Open MiningMetadata and Data Integration, XML XPATH, 
  JDBC SQL Swing TableModel, POJO, Hibernate HQL, and OLAP MDX.
* These days, there's need to spread reports across more and more populous groups. All of them need reports, but each 
  of them works in a different way using different software. Therefore it's so important to use a reporting tool 
  supporting **various output formats**. Just like Open Mining. No matter whether we need Excel spreadsheets, 
  PDF documents, XMLs or CSV files. All these (and not only them) are supported by Open Mining Community.
* Sometimes we might need to change report's format quickly and avoid quality and form losses. The feature 
  responsible for that is **accurate formatting at the pixel level** which assure that all elements stay aligned. 
  Although it's not realizable in some cases, changes among three most popular formats (HTML, PDF and spreadsheets) 
  do not cause any noticeable modifications in report's appearance.
* The more complex reports we have to prepare the more attention we have to pay to its transparency and legibility. 
  Thereupon, most of reports include diverse **charts** that are **easy to embed** with Open Mining.
* All reports have to be as transparent as possible, therefore we should be provided with a possibility for 
  defining what ranges and values we want to see. Parameterization options of **Open Mining** are sufficient 
  for most uses.
* People used to attach weight to the number of data included in a report. Nonetheless, the more data we 
  have the more complex and therefore unclear the report gets. Open Mining supports using sub- or **partial 
  reports** to relieve the main part.
* If there was a one file format better than the rest, for reporting it would be XLS. Excel spreadsheets 
  seem to be the ideal solution for presenting multiple data and information, therefore diverse reporting 
  tools, including Open Mining, allow their users to create reports that look like spreadsheets. They 
  usually are being called the cross tabs.
* The report's lifecycle isn't over in the moment of rendering. People used to forget about its importance, 
  nonetheless a possibility for later editing truly is useful. The **interactivity of reporting** provided by 
  Open Mining enable end users to have an influence on reports' form, too.
* Preparing a transparent report isn't simple, therefore what matter are **various authoring options**. 
  Open Mining provide its users with WYSIWYG editor to make preparing reports easy as pie.
* Open Mining is being supported with **Business Intelligence Server**, multiplying its functionality. 
  Thank to that, the option of ad hoc reporting is enabled. It's all enough to understand that the 
  best is not what you have to pay most for - all Open Mining solutions are free for all uses.
* **Python** of Open Mining makes the tool **easy for extending**. This, followed with **open source license** 
  *MIT*, make Open Mining the most easily-customizable tool in the market. We do not have to pay for any 
  extensions as they're being spread for free. Moreover, we might easily prepare them ourselves - it's 
  just a matter of practice and there's no system restrictions.
* Business needs evolve, reporting solutions have therefore to evolve, too. Unlike any other tool, 
  Open Mining is **being incessantly developed** if there was any feature missing we might predict it 
  to be added soon.


It's been told that there are plenty of diverse reporting solutions currently accessible in the market 
and Open Mining is only one of them. It's been also pointed that the choice of the best one depends on 
each customer's needs. Nonetheless, knowing Open Mining's gratuity, we might suppose it to take place 
in small and medium-sized companies at most.


More about OLAP cube
--------------------

A cube can be considered a generalization of a three-dimensional spreadsheet. For example, a company might wish to 
summarize financial data by product, by time-period, and by city to compare actual and budget expenses. Product, 
time, city and scenario (actual and budget) are the data's dimensions.

Cube is a shortcut for multidimensional dataset, given that data can have an arbitrary number of dimensions. The 
term hypercube is sometimes used, especially for data with more than three dimensions.

Each cell of the cube holds a number that represents some measure of the business, such as sales, profits, 
expenses, budget and forecast.

OLAP data is typically stored in a star schema or snowflake schema in a relational data warehouse or in a 
special-purpose data management system. Measures are derived from the records in the fact table and dimensions are 
