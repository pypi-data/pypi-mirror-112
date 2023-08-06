import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and visualizing a Gaussian distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file
    """

    def __init__(self, mu=0, sigma=1):
        Distribution.__init__(self, mu, sigma)

    def calculate_mean(self):
        """Function to calculate the mean of the data set.

        param:
            None

        :return: (float) mean of the data set.
        """

        self.mean = 1.0 * sum(self.data) / len(self.data)

        return self.mean

    def calculate_stdev(self, sample=True):
        """Function to calculate the standard deviation of the data set.

        :param sample: (bool) whether the data represents a sample or population.

        :return: (float) standard deviation of the data set
        """

        sum_deviations = sum([pow(x - self.calculate_mean(), 2) for x in self.data])

        if sample:
            self.stdev = math.sqrt(sum_deviations / (len(self.data) - 1))
        else:
            self.stdev = math.sqrt(sum_deviations / len(self.data))

        return self.stdev

    def plot_histogram(self, color="white"):
        """Function to output a histogram of the instance variable data using matplotlib pyplot library.

        :param color: (String) the color of the histogram.

        :return None:
        """
        plt.hist(self.data, edgecolor="black")
        plt.title('Histogram of Data')
        plt.xlabel('data')
        plt.ylabel('count')

    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.

        :param x: (float) point for calculating the probability density function

        :return: (float) probability density function output
        """

        return (1.0 / (self.stdev * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - self.mean) / self.stdev) ** 2)

    def plot_histogram_pdf(self, n_spaces=50):
        """Function to plot the normalized histogram of the data and a plot of the probability density function
        along the same range

        :param n_spaces: (int) number of data points

        :returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
        """

        min_range = min(self.data)
        max_range = max(self.data)

        # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval * i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2, sharex="True")
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Gaussian PyxDistributions

        :param other: (Gaussian) Gaussian instance

        :return: (Gaussian) Gaussian distribution
        """

        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)

        return result

    def __repr__(self):
        """Function to output the characteristics of the Gaussian instance

        param:
            None

        :return: (string) characteristics of the Gaussian
        """

        return "mean {}, standard deviation {}".format(self.mean, self.stdev)
