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
        print(f'After round {cnt}')
        print(done)
        print(waiting_time)

    print(waiting_time)
    print(time_stamp)

