import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import defaultdict
import random
class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.discount = 0.7
        self.current_iter = 1
        self.epsilon = 1 
        self.alpha = 0.6
        self.q_table = defaultdict(int)
        self.reward = 0
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.current_iter = 1   
        self.reward = 0 


    def update(self, t):
        # Gather inputs
        deadline = self.env.get_deadline(self)
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        
        # TODO: Update state
        state = inputs.items()
        state.extend([self.next_waypoint])
        self.state = tuple(state)
        valid_actions = self.env.valid_actions

        # TODO: Select action according to your policy
        #taking random action as a first requirement
        action = random.choice(valid_actions)
        if self.epsilon >0 :
            pass 
        else:
            action_value={}
            possible_values = []
            if len(self.q_table) == 0:
                for act in valid_actions:
                    self.q_table[self.state,act] = 0 
            else:     
                for key,value in self.q_table.items():
                    state = key[0]
                    if state == self.state:
                        action = key[1]
                        possible_values.append(value)
                        action_value[action] = value 

                if len(possible_values) == 0:
                    for act in valid_actions: 
                        self.q_table[self.state,act] = 0
                        action_value[act] = 0
                        possible_values.append(0)

                else:
                    max_value = max(possible_values)
                    for key,value in action_value.iteritems():
                        if value == max_value:
                            action = key

        # Execute action and get reward
        reward = self.env.act(self, action)
        
        if self.current_iter == 1 :
            self.prev_state = self.state
            self.prev_action = action
            self.prev_reward = reward

        # TODO: Learn policy based on state, action, reward
        self.q_table[self.prev_state,self.prev_action] = (1-self.alpha)*self.q_table[self.prev_state,self.prev_action] + self.alpha * (self.prev_reward + self.discount * self.q_table[self.state,action])
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        self.prev_action = action
        self.prev_state = self.state
        self.prev_reward = reward

        self.epsilon = self.epsilon - .02
        self.reward = self.reward + reward
        print(self.reward)
        self.current_iter = self.current_iter + 1 
 

def run():
    """Run the agent for a finite number of trials."""
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay= 0 )  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
