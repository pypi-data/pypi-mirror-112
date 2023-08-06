# Intersectionalipy

## Background

As debates about race, privilege, and cultural power continue to rage through our society, [intersectionality](https://en.wikipedia.org/wiki/Intersectionality) has become simultaneously one of the most important and least well understood paradigms of thought in the modern political environment. The term itself, originally coined by [Kimberlé Williams Crenshaw](https://en.wikipedia.org/wiki/Kimberl%C3%A9_Williams_Crenshaw), refers to ways in our overlapping identities influence our experiences of privilege and oppression.

At its core, intersectionality is a framework for describing how people's different identities interact and amplify each other in ways that not are simply described by single categories like race or gender. For instance, a Black woman might experience the condition of her race¹ differently than a Black man would. The theory aims to describe the different "vectors of oppression" that a person might experience as a result of their identities. At a community level, this results in the idea of a ["matrix of domination"](https://en.wikipedia.org/wiki/Matrix_of_domination) that describes the relationships between different strata of society.

In order to formalize this theory mathematically, we must clear up some potentially confusing terminology. We can consider the notion of oppression <img src="svgs/9afe6a256a9817c76b579e6f5db9a578.svg?invert_in_darkmode" align=middle width=12.99542474999999pt height=22.465723500000017pt/> to be a function over a set of identity values <img src="svgs/80af6ae18f698ba9f619c4eaf4bd5ebb.svg?invert_in_darkmode" align=middle width=96.64711814999998pt height=24.65753399999998pt/> drawn from a set of identity spaces <img src="svgs/86c97659c620ceaac8a8a66ffd7c06d7.svg?invert_in_darkmode" align=middle width=101.33558984999999pt height=24.65753399999998pt/>. While the output space of the oppression fuction may itself be mulitdimensional–economic, social, political, etc.–the term "vectors of oppression" is a bit of a misnomer as oppression does not properly constitue a [vector space](https://en.wikipedia.org/wiki/Vector_space) (for instance, addition of oppressions is not guaranteed to be commutative). Indeed, much of the work of intersectionality involves considering maps between different identities (not to be confused with the standard [idenity map](https://en.wikipedia.org/wiki/Identity_function) concept in mathematics, e.g. the [identity matrix](https://en.wikipedia.org/wiki/Identity_matrix) in the [general linear group](https://en.wikipedia.org/wiki/General_linear_group) <img src="svgs/486cbdd2d13274e54f9ae74098899d1c.svg?invert_in_darkmode" align=middle width=66.67854929999999pt height=24.65753399999998pt/>) to understand the oppression a person might experience if their identity were to be different (i.e., <img src="svgs/f77e5f9b4b03b5e4b2853d61d678cef6.svg?invert_in_darkmode" align=middle width=265.81727865pt height=24.65753399999998pt/>). In this formalism, we also realize that the "matrix of domination" is not properly a matrix, as it does not describe a linear transformation between identity spaces (it is more properly a [bivector](https://en.wikipedia.org/wiki/Bivector) of domination).

While it might seem a trivial observation that people from different backgrounds experience the world differently, the theory of intersectionality makes straightforward but strong mathematical claims that have significant implications in the realm of statistical analysis. Namely, intersectionality asserts that oppression *cannot* generally be expressed as a linear combination of functions over the individual subspaces (that is, functions of the form <img src="svgs/6287e8fd54e3d5f65b3a80ca823e3434.svg?invert_in_darkmode" align=middle width=102.28022309999999pt height=24.657735299999988pt/>). Rather, oppression must be considered as a general, possibly non-linear, function over the entire identity space, <img src="svgs/5797f62bdb7be6ea93dc70223f1e7904.svg?invert_in_darkmode" align=middle width=121.69416765pt height=24.65753399999998pt/>.

This leads to natural, practical consequences in the practices of [statistics](https://en.wikipedia.org/wiki/Statistics) and [econometrics](https://en.wikipedia.org/wiki/Econometrics). Most directly, it is frequent practice to run [regressions](https://en.wikipedia.org/wiki/Regression_analysis) which attempt to control for the effects of different identities through the use of [indicator/dummy variables](https://en.wikipedia.org/wiki/Dummy_variable_(statistics)) (or one-hot encodings in the machine learning parlance). Typically these indicator variables are produced at the level of a single identity space <img src="svgs/486a629ac629a4ab4efb8989e3b946d4.svg?invert_in_darkmode" align=middle width=14.35643219999999pt height=22.465723500000017pt/>. Such a formalism precludes the ability to capture the kind of non-linear interactions between identities that are the focus of intersectional analysis. Instead, intersectionality prescribes that these indicator variables should be constructed on the [Cartesian product](https://en.wikipedia.org/wiki/Cartesian_product) of the identity spaces. 

An aside: this distinction is especially crucial for regression and other linear approaches that are dominant in the social sciences. However, in the discipline of [machine learning](https://en.wikipedia.org/wiki/Machine_learning) (ML) more flexible models are common (like [random forests](https://en.wikipedia.org/wiki/Random_forest) and [neural networks](https://en.wikipedia.org/wiki/Neural_network)) which have the ability, in principle, to express arbitrary non-linear relationships. Thus, a valid ML approach is to use a non-linear model with the standard indicator identity variables. (We should be careful to distinguish this ML approach from another "ML" approach–that of [Marxism-Leninism](https://en.wikipedia.org/wiki/Marxism%E2%80%93Leninism), which would impose that oppression be a univariate function of class², itself possibly a function of identity.)

While the construction of indicator variables from the Cartesian product space is a powerful prescription, it doesn't come for free: namely, this construction invites the [curse of dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality). If we incorporate even a relatively small number of identity spaces like race, gender, and sexual orientation, we could easily end up with 100 indicator variables. Unless we are dealing with a large number of observations in our dataset, this in turn can lead to [overfitting](https://en.wikipedia.org/wiki/Overfitting), or in the extreme case to more fitting parameters than observations and thus [no unique solution](https://en.wikipedia.org/wiki/Underdetermined_system). Therefore, *intersectional analysis must carefully balance the inclusion of these interaction terms with the concern of statistically significant, generalizable results*. 

Intersectionalipy is a package for [Python](https://www.python.org/) that aims to make this kind of intersectional analysis easier for researchers.


¹Not to be confused with a [race condition](https://en.wikipedia.org/wiki/Race_condition), which is a rarely a concern in synchronous Python code due to the [global interpreter lock](https://en.wikipedia.org/wiki/Global_interpreter_lock).

²Function of class here meaning class in the political sense; intersectionalipy does not register any [methods](https://docs.python.org/3/tutorial/classes.html#method-objects) to existing Python classes.

## Usage
Intersectionalipy provides a clear, straightforward API that aims to simplify performing intersectional analysis in the scientific python stack. The package is built to work with [pandas](https://pandas.pydata.org/) DataFrames, which can plugged directly into statistical analysis packages like [statsmodels](https://www.statsmodels.org/stable/index.html) or [scikit-learn](https://scikit-learn.org/stable/index.html).

Intersectionalipy operates on DataFrames where some of the columns encode categorical identity information. Users pass in the dataframe and the names of those identity columns, and intersectionalipy returns a new dataframe where all identity columns have been replaced by a complete set of identity indicator variables.

For example:
```python
>>> import intersectionalipy as i14py, pandas as pd
>>> df = pd.DataFrame({
...     'data': [0.2, 0.7, 0.9],
...     'gender': ['female', 'male', 'female' ],
...     'race': ['white', 'Black', 'Asian'],
...     'sexuality': ['gay', 'straight', 'queer'],
... })
>>> df
   data  gender   race sexuality
0   0.2  female  white       gay
1   0.7    male  Black  straight
2   0.9  female  Asian     queer
>>> i14py.intersectionalize(df, ['race', 'sexuality', 'gender'])
   data  (Asian, queer, female)  (Black, straight, male)  (white, gay, female)
0   0.2                       0                        0                     1
1   0.7                       0                        1                     0
2   0.9                       1                        0                     0
```

If using all identity columns together results in too many indicator variables for a meaningful regression, researchers can choose to limit the set of identity interations they explore through multiple calls to intersectionalipy:
```python
df = i14py.intersectionalize(df, ['race', 'religion'])
df = i14py.intersectionalize(df, ['sexuality', 'gender'])
```
Practicioners may want to conduct a [power analysis](https://stats.idre.ucla.edu/other/mult-pkg/seminars/intro-power/) (as in statistical power, though the regression itself may be an analysis of cultural and political power) to decide on the right level of intersectionality.

NB: When running a regression on <img src="svgs/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode" align=middle width=14.99998994999999pt height=22.465723500000017pt/> categorical values with indicator variables, it is typical practice to use <img src="svgs/e35caf405a5e9b4afd75a0d338c4dc12.svg?invert_in_darkmode" align=middle width=43.31036984999999pt height=22.465723500000017pt/> indicator regressors to prevent overfitting. This is typically done by choosing one category to leave out, and then the coefficients on all other indicator variables are interpreted with respect to that left out category. Because the sensible choice of a base category often depends on the detailed nature of the problem, intersectionalipy leaves this choice to the researcher and returns all <img src="svgs/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode" align=middle width=14.99998994999999pt height=22.465723500000017pt/> indicators. 



## Installation

`pip install intersectionalipy`
