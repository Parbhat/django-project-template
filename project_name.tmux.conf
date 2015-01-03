tmux has-session -t {{ project_name }}
if [ $? != 0 ]
then
    tmux new-session -s {{ project_name }} -n vim -d
    tmux send-keys -t {{ project_name }} 'workon {{ project_name }}' C-m
    tmux new-window -n shell/server -t {{ project_name }}
    tmux send-keys -t {{ project_name }} 'workon {{ project_name }}' C-m
    tmux new-window -n etc -t {{ project_name }}
    tmux send-keys -t {{ project_name }} 'workon {{ project_name }}' C-m
    tmux select-window -t {{ project_name }}:1
fi
tmux attach -t {{ project_name }}
