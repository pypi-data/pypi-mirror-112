def load(*data):
    return data

def plot(data):
    print(data)

def run(self=None):
    if self is None:
        self = globals()

    load = self.get('load')  # else default load
    features = self.get('features')
    plot = self.get('plot')
    show = self.get('show')

    data = load(1,2,3)

    if plot: plot(data)
    
run()
