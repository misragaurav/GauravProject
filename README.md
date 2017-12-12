# GauravProject
Here's some background on the project:
This was a consulting project for Foresite. The company purchased and provided me with medical claims records for 2 new first-in-class diabetes drugs. They wanted me to dig up intel from this data to help with launch of a new diabetes drug (the product of one of their portfolio companies). The deliverables were insights and codes. 

Couple of highlights of my approach to the project are:
1. I figured out that the the data they gave me had very little predictive value by itself. So, I improvised to supplement their data with free data from multiple public sources: the CMS.gov website, American diabetes association website, and the US census website.
2. I couldn't get over 65% accuracy in my predictions while considering the two drugs separately. I realized that the sales and marketing efforts of the companies of the two drugs had biased the individual datasets such than non-predictive features (like geographical regions) had become overtly important. So, I took an intersection of the two drugs' datasets to wash out the company-specific biases and got a 10% jump in my prediction accuracy right away.

Here is the presentation I created to summarize the project:
http://bit.ly/2kfL70c
I'll be happy to walk you through this whenever you have 10 minutes to spare.

I had only 3 weeks to get this all done.

Some notes regarding the codes:

The top level files are:
script_ML.py
script_analytics.py

As the names suggest, the script_ML contains the machine learning pipeline and the script_analytics contains the analytics code. The first 150 lines are common across the two scripts because both need the same data pre-processing. I could have written a function to capture those 150 lines of common code but the ROI is small on that and the readability of the code will reduce. I've included the analytics code at the bottom of the script_ML as well for when I want to run analytics after doing ML.

There are several functions spread across several files. All files containing functions have names starting with 'func_' followed by an elaborate name that summarizes what the function does. Each function file has doc string summary on the top.

For running this pipeline:
1. I've used plotly's online services for choropleths. To plot the choropleths, you'll need to use your own credentials in the file func_plotly_choropleth.
2. The randomized grid search takes about 4 minutes to search in the current setup on my laptop.
3. Plotting the ROC curve using the model fitted with randomized grid search and stratifying the full data into 6 sets takes about 12 minutes.
