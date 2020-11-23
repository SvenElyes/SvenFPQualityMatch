#we get a hist file as a an input and try to visualize it.
import os
import matplotlib.pyplot as plt


from matplotlib import pyplot as plt


all_histos=sorted(os.listdir('./histoSummary/'))
all_histos.remove('.DS_Store')
path='./histoSummary/'
summary_dict={}
'''fill the summary dict with information. THe key is the name of the file, afterwards it has the format: found cars, not found cars, and developement'''
for histo in all_histos:
    #print(histo)
    f= open(f"{path}{histo}", "r")
    car_counter=0
    not_car_counter=0
    entwicklung = []
    for x in f:
        #print(x)
        if "Car" in x:
            car_counter= car_counter +1
            entwicklung.append(1)
        else:
            not_car_counter = not_car_counter + 1
            entwicklung.append(0)
    summary_dict[histo]=(car_counter,not_car_counter,entwicklung)
    #print(car_counter, not_car_counter)
#for element in summary_dict:

plot_name=[]
plot_car=[]
plot_no_car=[]
plot_car_percent=[]
plot_car_devo=[]
for element in summary_dict:
    content= summary_dict[element]
    plot_car.append(content[0])
    plot_no_car.append(content[1])
    plot_name.append(element[:-23])
    plot_car_devo.append(content[2])


def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())
    
'''
print(plot_name)
print(plot_car)
for i in range (0,22,5):
    
    if i ==20:
        x=plot_name[i:i+3]
        y=plot_car[i:i+3]
        z=plot_no_car[i:i+3]
        
        
        data = {
        "cars found": y,
        "cars not found": z,
        }

        fig, ax = plt.subplots()
        bar_plot(ax, data, total_width=.8, single_width=.9)
        plt.xticks(range(3), x,rotation=90)
        plt.tight_layout()
        plt.savefig(f"Figures/{i/5}.png")
        
    else:
        
        x=plot_name[i:i+5]
        y=plot_car[i:i+5]
        z=plot_no_car[i:i+5]
        
        data = {
        "cars found": y,
        "cars not found": z,
        }

        fig, ax = plt.subplots()
        bar_plot(ax, data, total_width=.8, single_width=.9)
        plt.xticks(range(5), x,rotation=90)
        plt.tight_layout()
        plt.savefig(f"Figures/{i/5}.png")
'''
big_devo_array=[]
for devo in plot_car_devo:
    
    positive=0
    negative=0
    rate_array=[]
    for element in devo:
        if element ==1:
            positive=positive+1
        if element ==0:
            negative=negative+1
        rate= positive/(positive+negative)
        rate_array.append(rate)
    big_devo_array.append(rate_array)
counter= 1
for index in range(len(big_devo_array)):

    element=big_devo_array[index]
    plt.plot(element)
    plt.savefig(f"Figures/entwicklung{counter}.png")
    counter=counter +1
