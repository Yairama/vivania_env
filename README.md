# vivania_env

<p>
  <a href="https://www.linkedin.com/in/yairama/" rel="nofollow noreferrer">
    <img src="https://i.stack.imgur.com/gVE0j.png" alt="linkedin" class="icon" width="20" height="20"> LinkedIn
  </a> &nbsp; 
  <a href="https://github.com/Yairama" rel="nofollow noreferrer">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="github" class="icon" width="20" height="20"> Github
  </a> &nbsp; 
  <a href="https://gitlab.com/Yairama" rel="nofollow noreferrer">
    <img src="https://cdn-icons-png.flaticon.com/512/5968/5968853.png" alt="gitlab" class="icon" width="20" height="20"> Gitlab
  </a>
</p>

### This is one of my favourite projects
#### The project is composed of two repositories, vivania_env and vivania_learn, one contains the environment and the other contains the training code.

*Text originally extracted from my [linkedin publication](https://www.linkedin.com/posts/yairama_mineraeda-reinforcementlearning-artificialintelligence-activity-6937107270790975488-0tco?utm_source=share&utm_medium=member_desktop)*

Artificial Intelligence - Enhanced learning applied to mining fleet management.

Greetings!!!

Some time ago I decided that I wanted to go down the path of Mining AI Engineer, so I went into supervised, unsupervised learning. Finally, I decided it was time to go a bit further, and started on the path of reinforced learning applied to #mining.

I was developing a project by way of learning, which consists of an artificial intelligence that learns from scratch and by itself the most basic of fleet management: assigning trucks to destination zones. I decided to call the AI Vivania.

The results were very good (for the short time the AI had to train) and exceeded my expectations, however, they are still far from ideal, but with the right improvements and the right training it can go very far, so I decided to share a video of how the AI evolved and also the source code so you can use it as you like.

Considerations:
1. The AI trained a little (approx. 1 day) because I don't have an Nvidia GPU I trained with the CPU.
2. The project is modular and is divided in 2 repositories: vivania_env and vivania_learn, being the first one the environment where the AI will train (a kind of simulator) and the second one the algorithms and scripts that the AI used to train, where the first one can be used independently as a simulator while the second one depends on the first one.
3. The simulator takes into account many parameters such as: equipment efficiency, loading and emptying speeds, speed per track section, hang, queue (loading and unloading), hopper capacity, etc. (for more details check the code).
The algorithms used for training were A2C, PPO and TD3 modified for discrete action spaces, the latter being the one that yielded the best results, however, this algorithm is not ideal for this type of work.
5. You are totally free to do whatever you want with the code if it can be useful to you, just don't forget to leave credits ;).

Results:
Vivania learned to direct trucks to the loading zones when they were empty, and then to the unloading points when they were loaded.
Vivania was not able to reduce the Hang efficiently, this is due to the short time she had to train, however, as the training progressed the accumulated Hang was reduced little by little.
Vivania learned to use "bugs" in the test environment to reduce the queue time of the trucks, leaving some unloaded trucks stationary in the unloading areas so that in this way it does not add up the queue times.
And many other results that I cannot write in this publication.

<video src='https://user-images.githubusercontent.com/45445692/230273468-a967f61a-85dd-4b85-85a2-314054e3e38b.mp4' width=720></video>
