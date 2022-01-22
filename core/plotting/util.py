def make_runtime_plot(runtime, name):

    print('Making runtime plot')

    import matplotlib.pyplot as plt
    plt.plot(runtime)
    plt.xlabel('Number of games')
    plt.ylabel('Time [seconds]')
    plt.savefig(f'plots/runtime_{name}.pdf')
    plt.savefig(f'plots/runtime_{name}.png')
