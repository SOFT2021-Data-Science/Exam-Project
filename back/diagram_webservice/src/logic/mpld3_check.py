import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins
from utils.aliases import OUT_DIR


# Testing. Yoinked from https://mpld3.github.io/examples/interactive_legend.html
def mpld3_check():

    np.random.seed(9615)
    # generate df
    N = 100
    df = pd.DataFrame(
        (0.1 * (np.random.random((N, 5)) - 0.5)).cumsum(0),
        columns=["a", "b", "c", "d", "e"],
    )

    # plot line + confidence interval
    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)

    for key, val in df.iteritems():
        (l,) = ax.plot(val.index, val.values, label=key)
        print(f"{val.index} {val.values}")
        ax.fill_between(
            val.index,
            val.values * 0.5,
            val.values * 1.5,
            color=l.get_color(),
            alpha=0.4,
        )

    # define interactive legend

    handles, labels = ax.get_legend_handles_labels()  # return lines and labels
    interactive_legend = plugins.InteractiveLegendPlugin(
        zip(handles, ax.collections),
        labels,
        alpha_unsel=0.5,
        alpha_over=1.5,
        start_visible=True,
    )
    plugins.connect(fig, interactive_legend)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interactive legend", size=20)

    # Html string
    return mpld3.fig_to_html(fig)
