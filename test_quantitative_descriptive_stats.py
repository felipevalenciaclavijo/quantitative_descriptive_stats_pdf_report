from quantitative_descriptive_stats import bin_size, describe_column,\
clt_check, qqplot_check, study_choice, col_skewness, col_boxplot,\
col_histogram, col_qqplot, pdf_report, accept_skew

from pytest import approx
import pytest
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import webbrowser

def test_bin_size():
    """Verify that the function works fine
    with 2 different csv files when calculating
    the bin size.
    Parameters: none
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test.csv")
    column = "number"
    
    assert len(df[column]) == 15
    assert bin_size(df, column) == approx(9.99615)

    df2 = pd.read_csv("test_datasets/qds_test2.csv")
    column2 = "number2"
    
    assert len(df2[column2]) == 8
    assert bin_size(df2, column2) == approx(7.90791)

def test_describe_column():
    """Verify that the function works fine
    with 2 different csv files when describing
    the column data.
    Parameters: none
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"

    description = describe_column(df, column) 
    data1=[i for i in description.index]
    data2=[(i) for i in description]
    text = ['count',
            'mean',
            'std',
            'min',
            '25%',
            '50%',
            'max']
    numbers = [8.000000,
            87.250000,
            20.373301857367856,
            50.0,
            82.5,
            98.5]

    for _ in text:
        assert _ in data1
    for _ in numbers:
        assert _ in data2

    df = pd.read_csv("test_datasets/qds_test.csv")
    column = "number"

    description = describe_column(df, column) 
    data1=[i for i in description.index]
    data2=[(i) for i in description]
    text = ['count',
            'mean',
            'std',
            'min',
            '25%',
            '50%',
            'max']
    numbers = [15.000000,
            60.53333333333333,
            22.71521411699552,
            33.0,
            43.5,
            56.0]

    for _ in text:
        assert _ in data1
    for _ in numbers:
        assert _ in data2

def test_clt_check():
    """Verify that the function works fine
    with 3 different csv files when determining
    normality based on CLT.
    Parameters: none
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test.csv")
    column = "number"
    
    assert len(df[column]) == 15
    assert clt_check(df, column) == "- Because the sample size is less than 30, we can NOT determine that the data have a normal distribution; which means that we need to execute a QQ Plot check to decide if the data is approximately normally distributed."

    df2 = pd.read_csv("test_datasets/qds_test2.csv")
    column2 = "number2"
    
    assert len(df2[column2]) == 8
    assert clt_check(df2, column2) == "- Because the sample size is less than 30, we can NOT determine that the data have a normal distribution; which means that we need to execute a QQ Plot check to decide if the data is approximately normally distributed."

    df3 = pd.read_csv("test_datasets/qds_test3.csv")
    column3 = "number3"

    assert len(df3[column3]) == 31
    assert clt_check(df3, column3) == "- Because the sample size is greater than or equal to 30, we can determine that the data is approximately normally distributed, we can be confident this data can be used, and that we can continue with further testing and study."

def test_qqplot_check():
    """Verify that the outcome message of
    the function works fine when the analyst
    selects Y for Yes and N for No for the
    QQ Plot revision.
    Parameters: none
    Return: nothing
    """
    assert qqplot_check("y") == "- The QQ Plot dots follow a linear shape; therefore, we can determine the sample to have an approximately normal distribution; based on that we decided this data can be used and we can proceed with further tests and studies."
    assert qqplot_check("n") == "- The QQ Plot dots do NOT follow a linear shape; therefore, we can not determine the sample to have an approximately normal distribution."

def test_study_choice():
    """Verify that the outcome message of
    the function works fine when the analyst
    selects Y for Yes and N for No for the
    study choice.
    Parameters: none
    Return: nothing
    """
    assert study_choice("y") == "- Even though we can not clearly determined the sample data to have a normal distribution we are going to continue with the study."
    assert study_choice("n") == "- Because there wasn't enough data to determine sample data normality, we are not going to continue with the study. In other words, this data is insufficient to perform statistical tests."

def test_col_boxplot(monkeypatch):
    """Verify that the result of the function
    is a jpg file called accordingly from the
    name of the column for the boxplot.
    Parameters: monkeypatch prevents
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"

    df2 = pd.read_csv("test_datasets/qds_test.csv")
    column2 = "number"
    
    # This will stop the plot.show(), so it won't cause any
    # distractions while performing the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    assert col_boxplot(df, column) == "number2_boxplot.jpg"
    assert col_boxplot(df2, column2) == "number_boxplot.jpg"

def test_col_histogram(monkeypatch):
    """Verify that the result of the function
    is a jpg file called accordingly from the
    name of the column for the histogram.
    Parameters: monkeypatch prevents
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"
    K = bin_size(df, column)

    df2 = pd.read_csv("test_datasets/qds_test.csv")
    column2 = "number"
    K2 = bin_size(df2, column2)
    
    # This will stop the plot.show(), so it won't cause any
    # distractions while performing the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    assert col_histogram(df, column, K) == "number2_histogram.jpg"
    assert col_histogram(df2, column2, K2) == "number_histogram.jpg"

def test_col_qqplot(monkeypatch):
    """Verify that the result of the function
    is a jpg file called accordingly from the
    name of the column for the QQ Plot.
    Parameters: monkeypatch prevents
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"

    df2 = pd.read_csv("test_datasets/qds_test.csv")
    column2 = "number"
    
    # This will stop the plot.show(), so it won't cause any
    # distractions while performing the test
    monkeypatch.setattr(plt, 'show', lambda: None)

    assert col_qqplot(df, column) == "number2_qqplot.jpg"
    assert col_qqplot(df2, column2) == "number_qqplot.jpg"

def test_col_skewness():
    """Verify that the result of the function
    is an approx number of the skewness and
    also the shape of the distribution.
    Parameters: none
    Return: nothing
    """
    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"

    df2 = pd.read_csv("test_datasets/qds_test.csv")
    column2 = "number"

    assert col_skewness(df, column) == approx((-1.4030833, 'Highly Left-skewed'))
    assert col_skewness(df2, column2) == approx((0.3841761, 'Bell-Shaped'))

# ----------------------------------------------------------------------------------------------------------
# I COMMENTED THIS ONE BECAUSE I COULDN'T FIGURE OUT
# HOW TO PREVENT IT FROM OPENING THE PDF IN THE WEB BROWSER
# YOU CAN REMOVE THE '#' AND THE TEST ACTUALLY WORKS BUT
# IT OPENS THE PDF REPORT 4 TIMES FOR SOME REASON I
# DON'T KNOW :( VERY ANNOYING!
 
# def test_pdf_report():
#     """Verify that the result of the function
#     is a pdf file that opens automatically in
#     the web browser.
#     Parameters: none
#     Return: nothing
#     """
#     df = pd.read_csv("qds_test2.csv")
#     column = "number2"
#     summary = describe_column(df, column)
#     text = "With a skewness of -1.403083 for the number2, we consider the shape of the distribution to be: Highly Left-skewed"
#     conclusion1 = "- Because the sample size is less than 30, we can NOT determine that the data have a normal distribution; which means that we need to execute a QQ Plot check to decide if the data is approximately normally distributed."
#     conclusion2 = "- The QQ Plot dots do NOT follow a linear shape; therefore, we can not determine the sample to have an approximately normal distribution."
#     conclusion3 = "- Even though we can not clearly determined the sample data to have a normal distribution we are going to continue with the study."

#     assert pdf_report(column, summary, text, conclusion1, conclusion2, conclusion3) == webbrowser.open("number2_qds.pdf")
#----------------------------------------------------------------------------------------------------------
    

# DESPITE ALL MY GOOD EFFORTS I WASN'T ABLE TO HANDLE THIS ONE
# I FIGURED A WAY TO IMPLEMENT THIS ONE BY CHANGING
# the "-v" to an "-s" in the pytest.main(["-v", "--tb=line", "-rN", __file__])
# WHICH ALLOWS THE USER THAT RUN THE TEST TO ADD THE INPUT NEEDED
# SO THE FOLLOWING TEST VERIFY MANY THINGS FROM THAT FUNCTION BUT
# NOT THE ACTUAL FUNCTION WITH IT'S OUTPUT :(
def test_accept_skew():
    """Verify that the text outcomes
    are the expected ones.
    Parameters: none
    Return: nothing
    """
    df2 = pd.read_csv("test_datasets/qds_test.csv")
    column2 = "number"
    skew, shape = col_skewness(df2, column2)

    text = f"With a skewness of {skew:.6f} for the {column2}, we consider\
        the shape of the distribution to be: {shape}"
    
    decision_skew = "y"
    if decision_skew == "y":
        assert text == "With a skewness of 0.384176 for the number, we consider\
        the shape of the distribution to be: Bell-Shaped"
    
    
    final_decision_skew = ["Uniform", "Symmetric", "Unimodal", "Bimodal", "Multimodal"]

    text2 = f"Despite having a skewness of {skew:.6f} for the {column2}, we consider\
        the shape of the distribution to be: {final_decision_skew[0]}"

    text3 = f"Despite having a skewness of {skew:.6f} for the {column2}, we consider\
        the shape of the distribution to be: {final_decision_skew[1]}"
    
    assert text2 == "Despite having a skewness of 0.384176 for the number, we consider\
        the shape of the distribution to be: Uniform"

    assert text3 == "Despite having a skewness of 0.384176 for the number, we consider\
        the shape of the distribution to be: Symmetric"

    df = pd.read_csv("test_datasets/qds_test2.csv")
    column = "number2"
    skew2, shape2 = col_skewness(df, column)

    text4 = f"With a skewness of {skew2:.6f} for the {column}, we consider\
        the shape of the distribution to be: {shape2}"
    
    assert text4 == "With a skewness of -1.403083 for the number2, we consider\
        the shape of the distribution to be: Highly Left-skewed"
    
    
    final_decision_skew2 = ["Uniform", "Symmetric", "Unimodal", "Bimodal", "Multimodal"]

    text5 = f"Despite having a skewness of {skew2:.6f} for the {column}, we consider\
        the shape of the distribution to be: {final_decision_skew2[2]}"

    text6 = f"Despite having a skewness of {skew2:.6f} for the {column}, we consider\
        the shape of the distribution to be: {final_decision_skew2[3]}"

    assert text5 == "Despite having a skewness of -1.403083 for the number2, we consider\
        the shape of the distribution to be: Unimodal"

    assert text6 == "Despite having a skewness of -1.403083 for the number2, we consider\
        the shape of the distribution to be: Bimodal"

pytest.main(["-v", "--tb=line", "-rN", __file__])