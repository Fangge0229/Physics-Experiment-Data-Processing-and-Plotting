import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

class PhysicsDataProcessor:
    def __init__(self):
        self.x_data = []
        self.y_data = []
    
    def input_data(self):
        print("请输入数据，每行输入一个x和y，用空格分隔，输入q结束")
        while True:
            try:
                line = input("输入x y: ")
                if line.lower() == 'q':
                    break
                x, y = map(float, line.split())
                self.x_data.append(x)
                self.y_data.append(y)
            except ValueError:
                print("输入格式错误，请重新输入")
        
        self.x_data = np.array(self.x_data)
        self.y_data = np.array(self.y_data)
    
    def input_single_variable_data(self):
        """输入单变量数据，自动为其搭配1,2...的横坐标"""
        print("请输入单变量数据，数据间使用空格隔开，输入q结束")
        while True:
            try:
                line = input("输入数据: ")
                if line.lower() == 'q':
                    break
                # 解析空格分隔的数据
                values = [float(x) for x in line.split()]
                self.y_data.extend(values)
            except ValueError:
                print("输入格式错误，请重新输入")
        
        # 自动为y数据搭配1,2...的横坐标
        self.x_data = np.array(range(1, len(self.y_data) + 1))
        self.y_data = np.array(self.y_data)
        print(f"已输入{len(self.y_data)}个数据点，横坐标自动设置为1到{len(self.y_data)}")
    
    def input_data_from_list(self, x_list, y_list):
        self.x_data = np.array(x_list)
        self.y_data = np.array(y_list)
    
    def calculate_statistics(self):
        if len(self.x_data) == 0:
            print("请先输入数据")
            return
        
        # 计算平均值
        x_mean = np.mean(self.x_data)
        y_mean = np.mean(self.y_data)
        
        # 计算方差
        x_var = np.var(self.x_data)
        y_var = np.var(self.y_data)
        
        # 最小二乘法拟合
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.x_data, self.y_data)
        
        # 计算相关系数r的平方
        r_squared = r_value ** 2
        
        # 计算标准误差
        residuals = self.y_data - (slope * self.x_data + intercept)
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        
        statistics = {
            'x_mean': x_mean,
            'y_mean': y_mean,
            'x_var': x_var,
            'y_var': y_var,
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'r_squared': r_squared,
            'std_err': std_err,
            'rmse': rmse
        }
        
        return statistics
    
    def generate_plot(self, save_path=None):
        if len(self.x_data) == 0:
            print("请先输入数据")
            return
        
        # 计算拟合线
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.x_data, self.y_data)
        fit_line = slope * self.x_data + intercept
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 绘制图像
        fig = plt.figure(figsize=(10, 6))
        plt.scatter(self.x_data, self.y_data, label='原始数据', color='blue')
        plt.plot(self.x_data, fit_line, label=f'拟合直线: y = {slope:.4f}x + {intercept:.4f}', color='red')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('最小二乘法拟合')
        plt.legend()
        plt.grid(True)
        
        # 保存图像
        if save_path:
            try:
                # 展开路径中的~符号
                expanded_path = os.path.expanduser(save_path)
                # 确保目录存在
                os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
                plt.savefig(expanded_path, dpi=300, bbox_inches='tight')
                plt.close(fig)
                print(f"图像已保存到: {expanded_path}")
            except Exception as e:
                print(f"保存图像时出错: {e}")
                plt.close(fig)
        else:
            plt.show()
            plt.close(fig)
    
    def get_latex_formulas(self):
        if len(self.x_data) == 0:
            print("请先输入数据")
            return
        
        statistics = self.calculate_statistics()
        
        latex = f"""
        \\section{{统计结果}}
        
        \\subsection{{基本统计量}}
        \\begin{{align}}
        \\bar{{x}} &= {statistics['x_mean']:.4f} \\\\
        \\bar{{y}} &= {statistics['y_mean']:.4f} \\\\
        \\sigma_x^2 &= {statistics['x_var']:.4f} \\\\
        \\sigma_y^2 &= {statistics['y_var']:.4f}
        \\end{{align}}
        
        \\subsection{{最小二乘法拟合}}
        \\begin{{align}}
        y &= kx + b \\\\
        k &= {statistics['slope']:.4f} \\\\
        b &= {statistics['intercept']:.4f} \\\\
        r &= {statistics['r_value']:.4f} \\\\
        r^2 &= {statistics['r_squared']:.4f} \\\\
        \\text{{标准误差}} &= {statistics['std_err']:.4f} \\\\
        \\text{{均方根误差}} &= {statistics['rmse']:.4f}
        \\end{{align}}
        
        \\subsection{{拟合公式}}
        \\begin{{equation}}
        y = {statistics['slope']:.4f}x + {statistics['intercept']:.4f}
        \\end{{equation}}
        """
        
        return latex
    
    def show_menu(self):
        print("\n=== 物理实验数据处理程序 ===")
        print("1. 输入双变量数据(x,y)")
        print("2. 输入单变量数据(自动搭配横坐标1,2,...)")
        print("3. 显示统计结果")
        print("4. 生成拟合图像")
        print("5. 输出LaTex公式")
        print("6. 退出")
    
    def run(self):
        self.show_menu()
        
        while True:
            choice = input("\n请选择功能 (1-6): ")
            
            if choice == '1':
                self.input_data()
            elif choice == '2':
                self.input_single_variable_data()
            elif choice == '3':
                stats = self.calculate_statistics()
                if stats:
                    print("\n=== 统计结果 ===")
                    print(f"x平均值: {stats['x_mean']:.4f}")
                    print(f"y平均值: {stats['y_mean']:.4f}")
                    print(f"x方差: {stats['x_var']:.4f}")
                    print(f"y方差: {stats['y_var']:.4f}")
                    print(f"斜率: {stats['slope']:.4f}")
                    print(f"截距: {stats['intercept']:.4f}")
                    print(f"相关系数r: {stats['r_value']:.4f}")
                    print(f"r平方: {stats['r_squared']:.4f}")
                    print(f"标准误差: {stats['std_err']:.4f}")
                    print(f"均方根误差: {stats['rmse']:.4f}")
            elif choice == '4':
                save_path = input("请输入保存路径（留空则直接显示）: ")
                self.generate_plot(save_path if save_path else None)
            elif choice == '5':
                latex = self.get_latex_formulas()
                if latex:
                    print("\n=== LaTex公式 ===")
                    print(latex)
                    save_latex = input("是否保存到文件？(y/n): ")
                    if save_latex.lower() == 'y':
                        latex_path = input("请输入保存路径: ")
                        # 展开路径中的~符号
                        expanded_latex_path = os.path.expanduser(latex_path)
                        with open(expanded_latex_path, 'w', encoding='utf-8') as f:
                            f.write(latex)
                        print(f"LaTex公式已保存到: {expanded_latex_path}")
            elif choice == '6':
                print("程序退出")
                break
            else:
                print("输入错误，请重新选择")
            
            # 每次操作后重新显示菜单
            self.show_menu()

if __name__ == "__main__":
    processor = PhysicsDataProcessor()
    processor.run()
