'''
n -> number of fog nodes
i -> index of fog node
m -> number of tasks (number of end node)
j -> index of task

done(j) -> indicates that task j is done
communication_cost(i,j) -> communication cost of ith fog node with jth ED
completion_time(i,j) -> time for completion of jth task on ith node
waiting_time(i) -> waiting time on ith fog node

O(j) -> preference list of jth task ->
O(j)(i) -> 1/omega(i,task_being_performed_at(i)) + epsilon(i,j)
D(i) -> preference list of ith node
D(i)(j) -> 1/omega(i,task_being_performed_at(i)) + epsilon(i,j) + phsi(j,i)

allocation_matrix(i,j) -> it is 1 if task j is being performed at ith node
request[i] -> stores a list of request to ith fog node

'''

import pygame
from pygame.locals import *

import random

import sys

# Constants
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

X_LIMIT = 1000
Y_LIMIT = 1000

random.seed(0)



m = 3
n = 3
O = [[],[],[]]
D = [[0.0,0,0],[0,0,0],[0,0,0]]
done = [0,0,0]
waiting_time = [0,0,0]
communication_cost = [[1,2,1],[2,3,1],[1,2,4]]
completion_time = [[4,2,1],[4,5,6],[3,2,4]]
request = [[],[],[]]
time_stamp = []

def compute_task_preference_list():
    for j in range(0,m):
        tmp_list = []

        if done[j] == 1:
            O[j] = tmp_list
            continue

        for i in range(0,n):
            tmp_list.append([1.0/(waiting_time[i] + communication_cost[i][j]),i])
        tmp_list.sort(reverse=True)
        O[j] = tmp_list;

def compute_fog_node_preference_list():
    for i in range(0,n):

        for j in range(0,m):
            if done[j] == 1:
                D[i][j] = 0
                continue
            D[i][j] = 1.0/(waiting_time[i] + communication_cost[i][j] + completion_time[i][j])

def propose_to_preferred_node():
    for i in range(0,n): request[i] = []

    for j in range(0,m):
        if done[j] != 1:
            request[O[j][0][1]].append(j)

def accept_preference():
    for i in range(0,n):
        idx = -1
        val = 0
        for u in request[i]:
            if D[i][u] > val and done[u] == 0:
                val = D[i][u]
                idx = u

        if idx == -1:
            continue
        # task with idx id schedule at ith node with waiting time of waiting[i]
        done[idx] = 1
        time_to_end = completion_time[i][idx] + communication_cost[i][idx];
        time_stamp.append((idx,waiting_time[i], waiting_time[i] + time_to_end,i))
        waiting_time[i] += completion_time[i][idx] + communication_cost[i][idx]

# initialize pygame window
pygame.init()

FPS = 30
Ticker = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((1000, 1000))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Fog task offloading simulation")


class EndNode:
    def __init__(self, id, mx):
        self.id = id
        self.x = 100
        self.y = (Y_LIMIT - 200) * ((id+1) / mx)

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, RED, (self.x, self.y), 10)

class FogNode:
    def __init__(self, id, mx):
        self.id = id
        self.x = X_LIMIT - 100 + random.randint(-50, 50)
        self.y = (Y_LIMIT - 200) * ((id+1) / mx)

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, BLUE, (self.x, self.y), 10)

m = 3 # number of edge nodes
n = 3 # number of fog nodes

EDs = [EndNode(i, m) for i in range(m)]
FNs = [FogNode(i, n) for i in range(n)]

class Connection:
    def __init__(self, id, n1, n2):
        self.node1 = n1
        self.node2 = n2

    def draw(self):
        pygame.draw.line(
            DISPLAYSURF,
            WHITE,
            (self.node1.x, self.node1.y),
            (self.node2.x, self.node2.y)
        )

# edge list
connections = []

# connect edge nodes to corresponding fog nodes
for i in range(m):
    connections.append(Connection(i, EDs[i], FNs[i]))

# complete graph between fog nodes
for i in range(n):
    for j in range(i+1, n):
        print(f"connecting FN {i} to {j}")
        connections.append(Connection(len(connections), FNs[i], FNs[j]))


def mainloop(tuples=[(2, 0, 7, 1), (0, 0, 4, 2), (1, 0, 4, 0)]):
    # tuples of (from, start_time, end_time, to)

    t = -1
    font = pygame.font.Font('freesansbold.ttf', 32)
    ED_label = font.render("End Nodes", True, BLACK, WHITE)
    FN_label = font.render("Fog Nodes", True, BLACK, WHITE)


    while True:
        DISPLAYSURF.fill(BLACK)

        for connection in connections:
            connection.draw()
        for ed in EDs:
            ed.draw()
        for fn in FNs:
            fn.draw()

        text = font.render(f"T = {t}", True, RED, BLACK)
        textRect = text.get_rect()
        DISPLAYSURF.blit(text, textRect)
        DISPLAYSURF.blit(ED_label, (80, 100))
        DISPLAYSURF.blit(FN_label, (X_LIMIT-180, 100))

        # task offloading lines in red
        for (FN_i, start_t, end_t, ED_i) in tuples:
            if start_t <= t <= end_t:
                pygame.draw.line(
                    DISPLAYSURF,
                    RED,
                    (FNs[FN_i].x, FNs[FN_i].y),
                    (EDs[ED_i].x, EDs[ED_i].y)
                )

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    t += 1
                    print(t)


        Ticker.tick(FPS)

if __name__ == '__main__':

    cnt = 0
    while True:
        fl = 1
        for j in range(0,m):
            if done[j] == 0: fl = 0

        if fl:
            break;

        compute_task_preference_list()
        compute_fog_node_preference_list()
        propose_to_preferred_node()
        accept_preference()

        cnt += 1
        # print(f'After round {cnt}')
        # print(done)
        # print(waiting_time)

    # print(waiting_time)
    # print(time_stamp)

    mainloop(time_stamp)
