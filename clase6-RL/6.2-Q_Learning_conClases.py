from gym.envs.toy_text import discrete
from io import StringIO


class CliffWalkingEnv(discrete.DiscreteEnv):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    metadata = {'render.modes': ['human', 'ansi']}

    def _limit_coordinates(self, coord):
        coord[0] = min(coord[0], self.shape[0] - 1)
        coord[0] = max(coord[0], 0)
        coord[1] = min(coord[1], self.shape[1] - 1)
        coord[1] = max(coord[1], 0)
        return coord

    def _calculate_transition_prob(self, current, delta):
        new_position = np.array(current) + np.array(delta)
        new_position = self._limit_coordinates(new_position).astype(int)
        new_state = np.ravel_multi_index(tuple(new_position), self.shape)
        reward = -100.0 if self._cliff[tuple(new_position)] else -1.0
        is_done = self._cliff[tuple(new_position)] or (tuple(new_position) == (3,11))
        return [(1.0, new_state, reward, is_done)]

    def __init__(self):
        self.shape = (4, 12)

        nS = np.prod(self.shape)
        nA = 4

        # Cliff Location
        self._cliff = np.zeros(self.shape, dtype=np.bool)
        self._cliff[3, 1:-1] = True

        # Calculate transition probabilities
        P = {}
        for s in range(nS):
            position = np.unravel_index(s, self.shape)
            P[s] = { a : [] for a in range(nA) }
            P[s][self.UP] = self._calculate_transition_prob(position, [-1, 0])
            P[s][self.RIGHT] = self._calculate_transition_prob(position, [0, 1])
            P[s][self.DOWN] = self._calculate_transition_prob(position, [1, 0])
            P[s][self.LEFT] = self._calculate_transition_prob(position, [0, -1])

        # We always start in state (3, 0)
        isd = np.zeros(nS)
        isd[np.ravel_multi_index((3,0), self.shape)] = 1.0

        super(CliffWalkingEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human', close=False):
        self._render(mode, close)

    def _render(self, mode='human', close=False):
        if close:
            return

        outfile = StringIO() if mode == 'ansi' else sys.stdout

        for s in range(self.nS):
            position = np.unravel_index(s, self.shape)
            # print(self.s)
            if self.s == s:
                output = " x "
            elif position == (3,11):
                output = " T "
            elif self._cliff[position]:
                output = " C "
            else:
                output = " o "

            if position[1] == 0:
                output = output.lstrip() 
            if position[1] == self.shape[1] - 1:
                output = output.rstrip() 
                output += "\n"

            outfile.write(output)
        outfile.write("\n")





# In[6]:
import numpy as np
from collections import defaultdict, namedtuple
import itertools
from matplotlib import pyplot as plt
import pandas as pd
import sys


class Qlearning():
    
    EpisodeStats = namedtuple("Stats",["episode_lengths", "episode_rewards"])

    def __init__(self, env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1):
        self.env = env
        self.nA = env.action_space.n
        self.num_episodes = num_episodes
        self.discount_factor = discount_factor
        self.alpha = alpha
        self.epsilon = epsilon
        self.Q = defaultdict(lambda: np.zeros(self.nA))
        self.stats = self.EpisodeStats(
            episode_lengths=np.zeros(num_episodes),
            episode_rewards=np.zeros(num_episodes) )
        self.policy = self._make_epsilon_greedy_policy()
        
    def _make_epsilon_greedy_policy(self):
        """
        Crea una política epsilon-greedy basado en una q-función (función de valor estado-acción) y un epsilon dados.
        
        Argumentos:
            Q: un diccionario que mapea cada estado/observación s a un array de numpy Q[s] = array([v_0, v_1, ... , v_nA]) de longitud nA
            que para un índice a del array contiene el valor v_a de tomar la acción a en el estado s. 
            (en nuestra notación de la clase q(s,a))
             
            epsilon: probabilidad de seleccionar una acción aleatoria (obliga a explorar), valor entre 0 y 1.
            
            nA: número de acciones en el entorno
        
        Retorna:
            Una función que dada una observación como argumento, retorna una política (un array de numpy de longitud nA)
            con probabilidades para cada acción. La política es tal que toma la mejor acción según Q con probabilidad (1-epsilon)
            y toma una acción al azar con probabilidad epsilon 
        """
        def policy_fn(observation):
            A = np.ones(self.nA, dtype=float) * self.epsilon / self.nA
            best_action = np.argmax(self.Q[observation])
            A[best_action] += (1.0 - self.epsilon)
            return A
        return policy_fn

    def run(self):
        # policy = self._make_epsilon_greedy_policy() #make_epsilon_greedy_policy(Q, epsilon, env.action_space.n)
    
        for i_episode in range(self.num_episodes):
            # printear cada 100 episodios
            if (i_episode + 1) % 100 == 0:
                print("\rEpisodio {}/{}.".format(i_episode + 1, self.num_episodes), end="")
                sys.stdout.flush()
                
            # Resetear el ambiente y elegir una primera acción
            state = self.env.reset()
            action_probs = self.policy(state)
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            
            # Relalizar un paso en el ambiente
            # total_reward = 0.0
            for t in itertools.count():
                
                # Tomar un paso
    #             action_probs = policy(state)
    #             action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
                next_state, reward, done, _ = self.env.step(action)
    
                # elegir próxima acción 
                next_action_probs = self.policy(next_state)
                next_action = np.random.choice(np.arange(len(next_action_probs)), p=next_action_probs)
    
                # Actualizar las estadísticas
                self.stats.episode_rewards[i_episode] += reward
                self.stats.episode_lengths[i_episode] = t
                
                # Actualización TD
                best_next_action = np.argmax(self.Q[next_state])    
                ####### COMPLETAR #########
                self.Q[state][action] += self.alpha*( reward + self.discount_factor*self.Q[next_state][best_next_action] - self.Q[state][action] )
                    
                if done:
                    break
                
                action = next_action
                state = next_state
    
    def plot(self, smoothing_window=10, noshow=False):
        # Plot the episode length over time
        fig1 = plt.figure(figsize=(10,5))
        plt.plot(self.stats.episode_lengths)
        plt.xlabel("Episode")
        plt.ylabel("Episode Length")
        plt.title("Episode Length over Time")
        if noshow:
            plt.close(fig1)
        else:
            plt.show()
    
        # Plot the episode reward over time
        fig2 = plt.figure(figsize=(10,5))
        rewards_smoothed = pd.Series(self.stats.episode_rewards).rolling(smoothing_window, min_periods=smoothing_window).mean()
        plt.plot(rewards_smoothed)
        plt.xlabel("Episode")
        plt.ylabel("Episode Reward (Smoothed)")
        plt.title("Episode Reward over Time (Smoothed over window size {})".format(smoothing_window))
        if noshow:
            plt.close(fig2)
        else:
            plt.show()
    
        # Plot time steps and episode number
        fig3 = plt.figure(figsize=(10,5))
        plt.plot(np.cumsum(self.stats.episode_lengths), np.arange(len(self.stats.episode_lengths)))
        plt.xlabel("Time Steps")
        plt.ylabel("Episode")
        plt.title("Episode per time step")
        if noshow:
            plt.close(fig3)
        else:
            plt.show()
    
        return fig1, fig2, fig3




if __name__ == "__main__":
    
    env = CliffWalkingEnv()

    ql = Qlearning(env, 500)
    
    ql.run()
    ql.plot()



