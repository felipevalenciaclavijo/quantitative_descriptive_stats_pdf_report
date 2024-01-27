"""
This program helps data analysts understand the data they have
specific things this function does:
1) Get Numerical Summaries
2) Obtain the 5 Number Summary with a Box Plot
3) Determine the Shape and distribution of the data with Histogram & Q-Q Plot
and helps the analyst make decisions to end up with a final conclusion of the
descriptive statistics analysis.
4) Creates a professional looking PDF report
"""
# The cereal.csv dataset I submitted is under License (CC BY-SA 3.0).
# License: https://creativecommons.org/licenses/by-sa/3.0/
# This has been gathered and cleaned up by Petra Isenberg, Pierre Dragicevic,
# and Yvonne Jansen. I found it on kaggle and here is a link to the original
# source: https://perso.telecom-paristech.fr/eagan/class/igr204/datasets

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import math
from scipy import stats
import scipy.stats as st
from statsmodels.graphics.gofplots import qqplot
from fpdf import FPDF
import webbrowser, os

# Branding Colors:

color1 = "#FDC100" #RGB = 56, 58, 89
color2 = "#383A59"
color3 = "#000000"
color4 = "#9D9EB4"

def main():

    try:
        # Print Instructions:
        print("Hello!\
        \nTo be able to use this automated process for quantitative\
        \ndescriptive analysis you need a CSV file that has at least 1\
        \ncolumn made of numbers. For your convenience you can use the\
        \ncereal.csv I submitted.\
        \nYou need to know the name of the column; for example, within\
        \nthe cereal.csv you can try with: rating, calories, or potass.\
        \nFor the following questions asked you can answer randomly\
        \nunless you have some knowledge about statistical tests.\
        \n\
        \nThis should work with any CSV file, if you try with a small one\
        \nthat has less that 30 columns, you should see different questions.\
        \nYou can try this by using qds_test2.csv and column 'number'\
        \n\
        \n*PD: I also created 3 test CSVs (qds_test, qds_test2, qds_test3)\
        \nfiles that you'll need for the test.")
        
        # ask the user for tha name of the file
        filename = input("What is the name of the CSV file? (DO NOT include '.csv' at the end): ")
        # filename = "qds_test2.csv"

        # read the CSV using Pandas
        df = read_csv("datasets/"+ filename + ".csv")
        # print the dataframe to visualize it
        print(df)

        # select the quantitative column you want to analyze
        column = input("Which column with numbers do you want to analyze?: ")
        # column = "number2"
        
        #print the selected column
        print(df[column])

        # Discover Numerical Summaries
        # print the summary
        summary = describe_column(df, column)
        print(summary)

        # Create 5 Number Summary with a Box Plot from the selected
        # column and save it as a jpg file
        col_boxplot(df, filename, column)

        # Reference of variables:
        conclusion1 = ""
        conclusion2 = ""
        conclusion3 = ""

        # determine normal distribution through the CLT
        conclusion1 = clt_check(df, column)

        # Create a Q-Q Plot from the selected column data
        col_qqplot(df, filename, column)

        # if CLT wasn't appropiate, decide normality based on the QQ Plot
        num_observations = len(df[column])
        if num_observations < 30:
            answer = input("Do the QQ Plot dots follow a linear shape\
                \nto determine a normal distribution? (Y/N): ")
            conclusion2 = qqplot_check(answer)
            if answer == "n":
                study_decision = input("Since the previous tests have NOT\
                    \nbeen approved, do you still want to continue\
                    \nwith the study? (Y/N): ")
                conclusion3 = study_choice(study_decision)
            else:
                conclusion3 = ""
        else:
            conclusion2 = ""

        # Determine bin size with Sturge’s Rule for our histogram
        K = bin_size(df, column)

        # Create a Histogram from the selected column with bin size
        col_histogram(df, filename, column, K)

        # Call the skewness function to determine the shape of the distribution
        skew, shape = col_skewness(df, column)
        skew_choice = f"With a skewness of {skew:.6f} for the {column}, we consider\
                \nthe shape of the distribution to be: {shape}"
        print(skew_choice)

        # Call the accept_skew function for the analyst to decide wheter to
        # accept the skew_choice or manually determine it:
        text = accept_skew(skew, column, shape)
        # Print automated text:
        print(text)

        # Creates and open a pdf report with the nummerical summary, the 3 images generated
        # previously, and the text conclusion for the shape of the distribution
        pdf_report(filename, column, summary, text, conclusion1, conclusion2, conclusion3)


    except (FileNotFoundError, PermissionError) as error:
        print(type(error).__name__, error, sep=": ")



#-----------------------------------------------------------------------------
# FUNCTIONS:

def read_csv(filename):
    """
    This function reads a csv with pandas
    Parameters:
        filename: the selected file
    returns data frame
    """
    df = pd.read_csv(filename)

    return df

def describe_column(df, column):
    """
    This function helps to discover
    Numerical Summaries
    Parameters:
        df: data frame
        column: the selected column
    returns a summary tab with pandas
    """
    summary = df[column].describe()
    return summary

def clt_check(df, column):
    """
    This function determines if the sample
    data can be determined normally
    distributed based on the Central Limit
    Theorem (CLT)
    Parameters:
        df: data frame
        column: the selected column
    returns a message with a conclusion
    """
    num_observations = len(df[column])
    if num_observations >= 30:
        message = "- Because the sample size is greater than or equal to 30, we can determine that the data is approximately normally distributed, we can be confident this data can be used, and that we can continue with further testing and study."
    else:
        message = "- Because the sample size is less than 30, we can NOT determine that the data have a normal distribution; which means that we need to execute a QQ Plot check to decide if the data is approximately normally distributed."
    return message

def qqplot_check(answer):
    """
    This function helps to decide if the sample
    data can be determined to have a normal
    distribution based on the QQ Plot dots
    Parameters:
        answer: Y for Yes and N for No
    returns a message with a conclusion
    """
    if answer.lower() == "y":
        message = "- The QQ Plot dots follow a linear shape; therefore, we can determine the sample to have an approximately normal distribution; based on that we decided this data can be used and we can proceed with further tests and studies."
    elif answer.lower() == "n":
        message = "- The QQ Plot dots do NOT follow a linear shape; therefore, we can not determine the sample to have an approximately normal distribution."
    return message

def study_choice(study_decision):
    """
    This function is for making a a decision
    of wheter to accept the data as normally
    distributed or not
    Parameters:
        answer: Y for Yes and N for No
    returns a message with a conclusion
    """
    if study_decision == "y":
        message = "- Even though we can not clearly determined the sample data to have a normal distribution we are going to continue with the study."
    elif study_decision == "n":
        message = "- Because there wasn't enough data to determine sample data normality, we are not going to continue with the study. In other words, this data is insufficient to perform statistical tests."
    return message

def col_boxplot(df, filename, column):
    """
    This function creates and saves a boxplot
    Numerical Summaries
    Parameters:
        df: data frame
        filename: the name of the csv file
        column: the selected column
    returns a boxplot image in jpg
    """
    fig = plt.figure(figsize =(3, 4))
    boxplot = plt.boxplot(df[column], patch_artist=True,
            boxprops=dict(facecolor=color4, color=color3),
            capprops=dict(color=color3),
            whiskerprops=dict(color=color3),
            flierprops=dict(color=color3,
            markeredgecolor=color2),
            medianprops=dict(color=color3))

    # Set title
    plt.title(label="Box Plot",
          loc="center",
          fontstyle='normal')
    # change the name of the tick label from 1 to the name of the column
    plt.xticks([1], [column])
    boxplot_image = f"{filename}_{column}_boxplot.jpg"
    plt.savefig("images/" + boxplot_image) # save as jpg
    plt.show()

    return boxplot_image

def bin_size(df, column):

    num_observations = len(df[column])
    bin_size = 1 + 3.322 * math.log(num_observations)
    # print(bin_size)
    return bin_size

def col_histogram(df, filename, column, K):
    """
    This function creates and saves a histogram
    Parameters:
        df: data frame
        filename: the name of the csv file
        column: the selected column
    returns a histogram image in jpg
    """
    # Create a Histogram with the bin size
    fig = plt.figure(figsize =(8, 4))
    histogram = plt.hist(df[column], bins = round(K), color = color4)
    # Set title
    plt.title(label="Histogram",
          loc="center",
          fontstyle='normal')
    plt.ylabel("frequency")
    plt.xlabel(f"{column}")

    histogram_image = f"{filename}_{column}_histogram.jpg"
    plt.savefig("images/" + histogram_image) # save as jpg
    plt.show()

    return histogram_image

def col_skewness(df, column):
    """
    This function computes the skewness with pandas
    Parameters:
        df: data frame
        column: the selected column
    returns skew: number result
            shape: the shape of the distribution
            based on the skew
    """
    skew = df[column].skew()

    if skew <= -1:
        shape = "Highly Left-skewed"
    elif skew <= -0.5:
        shape = "Moderately Left-skewed"
    elif -0.5 < skew < 0.5:
        shape = "Bell-Shaped"
    elif skew >= 1:
        shape = "Highly Right-skewed"
    elif skew >= 0.5:
        shape = "Moderately Right-skewed"

    return skew, shape

def accept_skew(skew, column, shape):
    """
    This function helps the analyst to accept or correct
    the shape of the distribution computed based on the
    function col_skewness
    Parameters:
        skew: skewness number
        column: the selected column
        skew_choice: a generic text string created with
        the skew and the column name
    returns text: a generic text string with the accepted
    skewness and shape
    """
    decision_skew = ""
    final_decision_skew = ""
    options = ["y", "n"]
    new_decision = None
    options2 = [1, 2, 3, 4, 5]
    
    while decision_skew not in options:
            # Accept or deny the shape determined by the skewness function:
            decision_skew = input("Do you accept the shape of the distribution\
                \ndetermined by the program? (Y/N): ")

            if decision_skew.lower() == "y":
                text = f"With a skewness of {skew:.6f} for the {column}, we consider the shape of the distribution to be: {shape}"

            elif decision_skew == "n":
                
                while new_decision not in options2:
                    new_decision = int(input("Select a Shape. Write 1 for 'Uniform', 2 for 'Symmetric', 3 for 'Unimodal',\
                        \n4 for 'Bimodal', and 5 for 'Multimodal': "))

                    if new_decision == 1:
                        final_decision_skew = "Uniform"

                    elif new_decision == 2:
                        final_decision_skew = "Symmetric"

                    elif new_decision == 3:
                        final_decision_skew = "Unimodal"

                    elif new_decision == 4:
                        final_decision_skew = "Bimodal"

                    elif new_decision == 5:
                        final_decision_skew = "Multimodal"

                    else:
                        print("Typo error. Please try again!")
                    
                    text = f"Despite having a skewness of {skew:.6f} for the {column}, we consider the shape of the distribution to be: {final_decision_skew}"

            else:
                print("Typo error. Please try again with Y for yes and N for no")

    return text

def col_qqplot(df, filename, column):
    """
    This function creates and saves a Q-Q Plot
    Parameters:
        df: data frame
        filename: the name of the csv file
        column: the selected column
    returns nothing
    """
    fig = plt.figure(figsize =(8, 4))
    ax = fig.add_subplot(111)
    data_points = df[column]
    res = stats.probplot(data_points, plot=plt)

    #Dots
    # ax.get_lines()[0].set_marker("r")
    ax.get_lines()[0].set_markerfacecolor(color4)
    ax.get_lines()[0].set_color(color4)
    ax.get_lines()[0].set_markersize(4.0)

    #Line
    # ax.get_lines()[1].set_linewidth(12.0)
    ax.get_lines()[1].set_color(color3)
    plt.title("Q-Q Plot")
    plt.ylabel(f"Sample quantiles")
    plt.xlabel("Theoretical quantiles")
    qqplot_image = f"{filename}_{column}_qqplot.jpg"
    plt.savefig("images/" + qqplot_image) # save as jpg
    plt.show()

    return qqplot_image

def pdf_report(filename, column, summary, dis_shape, conclusion1, conclusion2, conclusion3):
    """
    This function creates and saves a PDF report of the analysis and decisions
    Parameters:
        column: the selected column
        summary: the summary obtained from the describe_column function
        text: the text that contains the shape of the distribution
        conclusion1: text about normal distribution based on CLT
        conclusion2: text about normal distribution based on QQ Plot
        conclusion3: text about the decision to make about normal
        distribution based on not accepting the QQ Plot analysis
    returns a PDF Report that opens in the web browser
    """
    title = f"Quantitative Descriptive Statistics for {column}"
        
    class PDF(FPDF):
        def header(self):
            #logo
            self.image("logos/Dataplicada_ICON.png", 10, 8, 15)
            # font
            self.set_font("helvetica", "B", 16)
            # Set color of text
            self.set_text_color(56, 58, 89)
            # title
            self.cell(195, 10, title, border=False, ln=1, align="C")
            # line break
            self.ln(20)
        # page footer
        def footer(self):
            self.set_y(-15)
            # set font
            self.set_font("helvetica", "", 8)
            # set font to color grey
            self.set_text_color(128, 128, 128)
            # Page number
            self.cell(0, 10, f"Page {self.page_no()}", align= "R")

    # Create the PDF REPORT:
    # Determine layout, unit of measurement, and format
    pdf = PDF("P", "mm", "letter")

    # Get total page numbers
    pdf.alias_nb_pages()
    # Set auto page break
    pdf.set_auto_page_break(auto=True, margin = 15)
    # Add a page
    pdf.add_page()
    # Specify font, type, and size
    pdf.set_font("helvetica", "B", 16)
    # Set color of text
    pdf.set_text_color(56, 58, 89)
    # Specify font, type, and size
    pdf.set_font("helvetica", "B", 12)
    # Set color of text
    pdf.set_text_color(56, 58, 89)
    pdf.cell(55, 15, "Nummerical Summary", ln=True, align="R")
    # Insert histogram image:
    histogram_image = f"images/{filename}_{column}_histogram.jpg"
    pdf.image(histogram_image, 70, 40, 150)
    # Insert boxplot image:
    boxplot_image = f"images/{filename}_{column}_boxplot.jpg"
    pdf.image(boxplot_image, 10, 140, 60)
    # Insert q-qplot image:
    qq_plot_image = f"images/{filename}_{column}_qqplot.jpg"
    pdf.image(qq_plot_image, 70, 140, 150)
    # Set color of text
    pdf.set_text_color(0, 0, 0)
    # add description text
    # Specify font, type, and size
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(55, 5, str(summary), align= "R")
    pdf.cell(80, 20, ln=True)
    pdf.cell(80, 10)
    # Specify font, type, and size
    pdf.set_font("helvetica", "B", 12)
    # Set color of text
    pdf.set_text_color(56, 58, 89)
    pdf.cell(90, 10, "Shape of the Distribution", ln=True)
    # Specify font, type, and size
    pdf.set_font("helvetica", "", 10)
    # Set color of text
    pdf.set_text_color(0, 0, 0)
    pdf.cell(80, 10)
    pdf.multi_cell(115, 5, dis_shape, align="L")
    pdf.cell(195, 80, ln=True)
    # Specify font, type, and size
    pdf.set_font("helvetica", "B", 12)
    # Set color of text
    pdf.set_text_color(56, 58, 89)
    pdf.cell(55, 10, "Conclusions", ln=True)
    # Specify font, type, and size
    pdf.set_font("helvetica", "", 10)
    # Set color of text
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(195, 5, conclusion1, align="L")
    pdf.cell(55, 1, ln=True)
    pdf.multi_cell(195, 5, conclusion2, align="L")
    pdf.cell(55, 1, ln=True)
    pdf.multi_cell(195, 5, conclusion3, align="L")


    pdf.output(f"reports/{filename}_{column}_qds.pdf", "F")

    path = f"reports/{filename}_{column}_qds.pdf"
    open_pdf_browser = webbrowser.open('file://' + os.path.realpath(path))

    return open_pdf_browser


if __name__ == "__main__":
    main()