# Quick level solver to verify all levels are solvable
import sys

LEVELS = [
  # Level 1: Tutorial - straight line
  {
    "w":4, "h":1,
    "grid1": [[4,0,0,2]],
    "grid2": [[5,0,0,3]],
    "goal": "一起向右移动三次"
  },
  # Level 2: Simple different paths
  {
    "w":3, "h":3,
    "grid1": [[4,0,1],[0,0,1],[0,0,2]],
    "grid2": [[5,0,0],[1,0,0],[1,0,3]],
    "goal": "路径不同但操作相同"
  },
  # Level 3: Different mazes, same solution
  {
    "w":4, "h":3,
    "grid1": [[4,0,1,1],[0,0,0,1],[1,0,0,2]],
    "grid2": [[5,0,0,0],[0,0,0,0],[1,1,0,3]],
    "goal": "看似不同的迷宫，却有相同的解法"
  },
  # Level 4: Longer path
  {
    "w":5, "h":3,
    "grid1": [[4,0,0,1,1],[1,1,0,0,1],[1,1,1,0,2]],
    "grid2": [[5,0,0,0,0],[1,0,0,1,0],[0,0,0,0,3]],
    "goal": "路径越长，思考越深"
  },
  # Level 5: Zigzag
  {
    "w":4, "h":4,
    "grid1": [[4,0,1,1],[0,0,1,1],[0,0,0,1],[1,0,0,2]],
    "grid2": [[5,0,0,0],[0,0,0,1],[0,0,0,1],[1,0,0,3]],
    "goal": "蜿蜒曲折的路径"
  },
  # Level 6: Divergent paths
  {
    "w":5, "h":4,
    "grid1": [[4,0,0,0,1],[1,1,0,0,1],[1,0,0,0,1],[1,0,0,0,2]],
    "grid2": [[5,0,0,0,0],[0,0,0,0,0],[1,1,1,0,0],[1,1,1,0,3]],
    "goal": "两个球走过完全不同的路"
  },
  # Level 7: Complex
  {
    "w":5, "h":5,
    "grid1": [[4,0,0,0,1],[0,1,0,0,1],[0,0,0,1,1],[1,0,0,0,1],[1,0,0,0,2]],
    "grid2": [[5,0,0,0,0],[0,0,0,0,0],[0,1,1,0,0],[0,0,0,0,0],[1,1,0,0,3]],
    "goal": "复杂度升级"
  },
  # Level 8: Grand
  {
    "w":6, "h":5,
    "grid1": [[4,0,0,0,1,1],[0,0,0,0,1,1],[0,0,0,0,0,1],[1,0,0,0,0,1],[1,0,0,0,0,2]],
    "grid2": [[5,0,0,0,0,0],[0,0,0,0,0,0],[1,1,1,1,0,0],[1,1,0,0,0,0],[1,1,0,0,0,3]],
    "goal": "终局之战"
  }
]

DX = {'up':0, 'down':0, 'left':-1, 'right':1}
DY = {'up':-1, 'down':1, 'left':0, 'right':0}
DIRS = ['up','down','left','right']

def bfs_solve(grid1, grid2, start1, start2, goal1, goal2, w, h, max_depth=50):
    """BFS to find a common solution for both mazes."""
    from collections import deque
    
    visited = set()
    q = deque()
    q.append((start1[0], start1[1], start2[0], start2[1], []))
    visited.add((start1[0], start1[1], start2[0], start2[1]))
    
    while q:
        x1, y1, x2, y2, path = q.popleft()
        
        if (x1, y1) == (goal1[0], goal1[1]) and (x2, y2) == (goal2[0], goal2[1]):
            return path
        
        if len(path) >= max_depth:
            continue
        
        for d in DIRS:
            nx1, ny1 = x1 + DX[d], y1 + DY[d]
            nx2, ny2 = x2 + DX[d], y2 + DY[d]
            
            valid1 = 0 <= nx1 < w and 0 <= ny1 < h and grid1[ny1][nx1] != 1
            valid2 = 0 <= nx2 < w and 0 <= ny2 < h and grid2[ny2][nx2] != 1
            
            if not valid1 and not valid2:
                continue
            
            if not valid1:
                nx1, ny1 = x1, y1
            if not valid2:
                nx2, ny2 = x2, y2
            
            state = (nx1, ny1, nx2, ny2)
            if state not in visited:
                visited.add(state)
                q.append((nx1, ny1, nx2, ny2, path + [d]))
    
    return None

def find_start_goal(grid, start_val, goal_val):
    start = goal = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == start_val:
                start = (x, y)
            elif cell == goal_val:
                goal = (x, y)
    return start, goal

print("=" * 50)
print("Verifying SPLIT levels...")
print("=" * 50)

all_ok = True
for i, lv in enumerate(LEVELS):
    grid1 = lv['grid1']
    grid2 = lv['grid2']
    w, h = lv['w'], lv['h']
    
    # Clean grids (remove start/goal markers)
    g1 = [[0 if c in (2,4) else c for c in row] for row in grid1]
    g2 = [[0 if c in (3,5) else c for c in row] for row in grid2]
    
    s1, goal1 = find_start_goal(grid1, 4, 2)
    s2, goal2 = find_start_goal(grid2, 5, 3)
    
    if not s1 or not goal1:
        print(f"Level {i+1}: ERROR - Missing start or goal in grid1")
        all_ok = False
        continue
    if not s2 or not goal2:
        print(f"Level {i+1}: ERROR - Missing start or goal in grid2")
        all_ok = False
        continue
    
    solution = bfs_solve(g1, g2, s1, s2, goal1, goal2, w, h)
    
    if solution:
        dir_symbols = {'up':'↑','down':'↓','left':'←','right':'→'}
        sol_str = ''.join(dir_symbols[d] for d in solution)
        print(f"Level {i+1}: ✓ Solvable in {len(solution)} moves: {sol_str}")
    else:
        print(f"Level {i+1}: ✗ UNSOLVABLE!")
        all_ok = False

print("=" * 50)
if all_ok:
    print("All levels are solvable! ✓")
else:
    print("Some levels need fixing! ✗")
    sys.exit(1)
