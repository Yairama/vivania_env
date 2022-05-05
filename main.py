from matplotlib import pyplot as plt

from VivaniaEnv import VivaniaEnv

if __name__ == '__main__':
    env = VivaniaEnv()
    env.reset()
    while True:
        # Take a random action
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

        env.render(mode="human")

        if done:
            break

    env.close()
