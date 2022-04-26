from matplotlib import pyplot as plt

from VivaniaEnv import VivaniaEnv

if __name__ == '__main__':
    env = VivaniaEnv()
    obs = env.reset()
    while True:
        env.render(mode="human")

