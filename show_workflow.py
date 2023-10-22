import subprocess
import os

def get_git_log():
    cmd = ['git', 'log', '--pretty=format:%h %p %an %s']
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.splitlines()

def get_branches_for_commit(commit_hash):
    cmd = ['git', 'branch', '--contains', commit_hash]
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    branches = result.splitlines()
    return [branch.strip('* ') for branch in branches]

def visualize_workflow():
    logs = get_git_log()
    for log in logs:
        parts = log.split(' ')
        hash_id = parts[0]
        parents = [part for part in parts[1:] if len(part) == 40]  # 40-character SHA-1 hash
        
        if len(parents) > 1:
            merge_info = "MERGE COMMIT"
        else:
            merge_info = "NORMAL COMMIT"
        
        author = parts[len(parents)+1]
        message = ' '.join(parts[len(parents)+2:])
        
        branches = get_branches_for_commit(hash_id)
        print(f"Commit: {hash_id} | Type: {merge_info} | Branches: {', '.join(branches)} | Author: {author} | Message: {message}")

if __name__ == "__main__":
    os.chdir('../invaders')
    visualize_workflow()
    os.chdir('../github_practice_evaluation')
