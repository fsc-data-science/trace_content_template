# Goal 
Goal of this file is to outline potential data visualization/dashboard templates that can do the following:
(1) Given a query & set of data, identify the appropriate data visualization for that data.
(2) Given a set of data visualizations & broad context, identify the appropriate template (layout of relevant panels/viz) for the context.

Available panels include:
<commentary> General commentary can include the goal of the report (if static and time bound analysis), the hypothesis investigated, broad context about the analysis, or even AI generated insights, outliers, or noticeable patterns derived from visualizations and tables.
<metric card> A single value (number, date, entity) with possibly a title, subtitle, caption; formatted appropriately.
<visualization> A highcharts visual most often one of: (stacked) bar chart, scatter plot, line chart, area chart. May include donut/pie chart, sankey diagram/flow chart, heatmap, histogram, etc. 
<table> Well formatted, readable columns with values in row, at a specific observation-level which can be up to 3 levels deep (e.g. day, token_symbol, day-token_symbol, day-token_symbol-size).

Overall, I want a variety of templates but it should always be as concise as possible, requiring the user to ask for more in-depth or additional value.


## Template 0: Minimal

This is a great default for simple analysis where a visual can change over time (underlying data grows/changes) 
and commentary can point out key trends, outliers, etc. Commentary should not be "what" the viz is (the viz will 
have a title and subtitle and axis titles for that) - but how to interpret it.
```
+----------------------------+
| <commentary>               |
+----------------------------+
+----------------------------+
| <visualization>            |
+----------------------------+
```

## Template 1: Simple Overview

Not my favorite default, as table can be often too much (I'd rather have my viz have strong hover over tooltips 
and good commentary). But a common format users may expect to see.
```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <metric    | <metric       |
| card>      | card>         |
+------------+---------------+
+----------------------------+
| <visualization>            |
+----------------------------+
+----------------------------+
| <table>                    |
+----------------------------+
```

## Template 2: Comparison

This is a great 1-2 punch template. The first Commentary can be useful to explain *why* two groups are worth comparing,
why 1 group may be ahead of the other, and provide strong background information. While the second Commentary 
can be more explicitly analytical of the trends, outliers, differences in trends, or key data to note (e.g., if 
one group is catching up or running away with the competition). In many cases you'll want both charts to have the 
same style and Y axis ranges.  
```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <visualization> | <visualization> |
+------------+---------------+
+----------------------------+
| <commentary>               |
+----------------------------+
```

## Template 3: Alternating Narrative

This is useful for a broad survey of a single entity where the visuals may 
include some advanced KPI/metrics that warrant a definition colocated. In these situations the first 
Commentary would provide background context and what "good" would look like across the visuals. 
While the side commentary would provide details on the specific metric shown in the visuals & local trends. 
Again, while commentary can define, it should not say "what" a visual is. The viz will have title, subtitle, axes titles, etc.  
```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <commentary> | <visualization> |
+------------+---------------+
+------------+---------------+
| <commentary> | <visualization> |
+------------+---------------+
+------------+---------------+
| <commentary> | <visualization> |
+------------+---------------+
```

## Template 4: Multi-Section Report

The most expansive Report style template. This is often best for analytics that is time-specific (ideally static). 
Refreshes can be find if commentary is updatable. You would typically use this template for a linear-narrative. For example 
If diving into lending markets on a specific chain you may start top level activity. Then break it down into something like 
deposits by tx size. Then go further on top assets by size. The report is meant to be read top to bottom, versus skimmed to a specific section. 

```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <metric    | <metric       |
| card>      | card>         |
+------------+---------------+
+----------------------------+
| <visualization>            |
+----------------------------+
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <metric    | <metric       |
| card>      | card>         |
+------------+---------------+
+----------------------------+
| <visualization>            |
+----------------------------+
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <metric    | <metric       |
| card>      | card>         |
+------------+---------------+
+----------------------------+
| <visualization>            |
+----------------------------+
```

## Template 5: Grid Dashboard

This is great for when the visualizations are self-explanatory for common metric(s) but a single visual would be too messy. 
For example when comparing multiple entities you may like a single stacked bar chart, but if each entity has its own subgroups 
then you may want 1 viz per entity showing the subgroups. 
Commentary is not always required when viz titles and axes are enough. 
```
+------------+---------------+
| <visualization> | <visualization> |
+------------+---------------+
+------------+---------------+
| <visualization> | <visualization> |
+------------+---------------+
```

## Template 6: Viz + Table

A strong minimalist template, where the table acts as a more concise, comparative set of metric card.
You could imagine commentary explaining a metric and identifying key trends/hypothesis, the visual 
showing the current state between several entities, and the table showing 1-3 summary stats per entity 
in 2 - 4 columns concisely (e.g., mean and total for entities shown weekly stats via a stacked bar chart.)
```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <visualization> | <table>  |
+------------+---------------+
```

## Template 7: Report Style

A concise report that may or may not be linear. May include a variety of metrics on the same entity. 
Useful for over-views of a situation, that are at the same level of depth.    
```
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <metric    | <visualization> |
| card>      |                |
+------------+---------------+
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <visualization> | <table>  |
+------------+---------------+
+----------------------------+
| <commentary>               |
+----------------------------+
+------------+---------------+
| <visualization> | <visualization> |
+------------+---------------+
```
