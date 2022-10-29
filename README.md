# Lưu Ý:
+ Có 3 branch, nên ai làm phần nào thì push code lên branch đó, đừng push qua branch khác. Branch `main` sẽ tổng hợp lại từ 2 branch còn lại:
```
1. main
2. learning
3. detecting
```
# Phân công:
    - Learning: Tấn, Lan, 
    - Detecting: No one

# Cách push code:
```shell
git init # dùng khi push lần đầu
git add .
git commit -m "thông điệp"
git remote add origin https://github.com/FloRRenn/muVuldepecker.git # dùng khi push lần đầu
git branch -M <tên branch> # branch learning hoặc detecting
git push -u origin main
```
