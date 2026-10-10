#include "tools/socket.hpp"
#include <QApplication>
#include <QMainWindow>
#include <QTimer>
#include <QDebug>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QValueAxis>
#include <QVBoxLayout>
#include <QLabel>
#include <deque>
#include <algorithm>
#include <numeric>
#include <unistd.h>
#include <sys/socket.h>
#include <errno.h>

QT_CHARTS_USE_NAMESPACE

class ServerWindow : public QMainWindow
{
	Q_OBJECT

public:
	ServerWindow(const std::string &ip, int port, QWidget *parent = nullptr)
		: QMainWindow(parent), server_socket_(), client_fd_(-1), timer_(new QTimer(this))
	{
		setWindowTitle("TCP 数据示波器 - 服务端");
		resize(1000, 600);

		// 绑定端口并开始监听
		if (!server_socket_.bind(ip, port))
		{
			qCritical() << "Failed to bind";
			QApplication::exit(1);
			return;
		}

		if (!server_socket_.listen(5))
		{
			qCritical() << "Failed to listen";
			QApplication::exit(1);
			return;
		}

		setup_ui();
		setup_chart();

		// 等待客户端连接（非阻塞方式通过定时器检查）
		QTimer::singleShot(100, this, &ServerWindow::accept_client);
	}

	~ServerWindow()
	{
		if (client_fd_ >= 0)
		{
			::close(client_fd_);
		}
	}

private slots:
	void accept_client()
	{
		client_fd_ = server_socket_.accept();
		if (client_fd_ < 0)
		{
			status_label_->setText("❌ 等待客户端连接失败");
			return;
		}

		status_label_->setText("✅ 客户端已连接，正在接收数据...");

		// 开始定时读取数据
		connect(timer_, &QTimer::timeout, this, &ServerWindow::read_data);
		timer_->start(50);  // 每50ms检查一次数据
	}

	void read_data()
	{
		int temp = 0;
		int n = ::recv(client_fd_, &temp, sizeof(temp), MSG_DONTWAIT);  // 非阻塞读取

		if (n == sizeof(temp))
		{
			// 更新数据缓冲区
			data_buffer_.push_back(temp);
			if (data_buffer_.size() > 20)
			{
				data_buffer_.pop_front();
			}

			// 更新图表
			update_chart();

			// 更新统计信息
			int max_val = *std::max_element(data_buffer_.begin(), data_buffer_.end());
			int min_val = *std::min_element(data_buffer_.begin(), data_buffer_.end());
			int avg_val = std::accumulate(data_buffer_.begin(), data_buffer_.end(), 0) / data_buffer_.size();

			stats_label_->setText(QString("当前值: %1  |  最大: %2  |  最小: %3  |  平均: %4")
									  .arg(temp)
									  .arg(max_val)
									  .arg(min_val)
									  .arg(avg_val));
		}
		else if (n == 0 || (n < 0 && errno != EAGAIN && errno != EWOULDBLOCK))
		{
			// 连接断开
			timer_->stop();
			status_label_->setText("❌ 客户端断开连接");
			::close(client_fd_);
			client_fd_ = -1;
		}
	}

private:
	void setup_ui()
	{
		QWidget *central = new QWidget(this);
		QVBoxLayout *layout = new QVBoxLayout(central);

		// 状态栏
		status_label_ = new QLabel("⏳ 正在等待客户端连接...", this);
		status_label_->setStyleSheet("QLabel { font-size: 14px; padding: 8px; background: #0F172A; color: #F8FAFC; border-radius: 4px; }");
		layout->addWidget(status_label_);

		// 图表视图（稍后创建）
		chart_view_ = new QChartView(this);
		layout->addWidget(chart_view_);

		// 统计信息
		stats_label_ = new QLabel("当前值: --  |  最大: --  |  最小: --  |  平均: --", this);
		stats_label_->setStyleSheet("QLabel { font-size: 16px; padding: 12px; background: #1E293B; color: #38BDF8; border-radius: 4px; }");
		layout->addWidget(stats_label_);

		setCentralWidget(central);
	}

	void setup_chart()
	{
		series_ = new QLineSeries();
		series_->setColor(QColor("#38BDF8"));  // 亮蓝色曲线

		QPen pen = series_->pen();
		pen.setWidth(3);
		series_->setPen(pen);

		chart_ = new QChart();
		chart_->addSeries(series_);
		chart_->setTitle("实时数据曲线");
		chart_->setTitleBrush(QBrush(QColor("#F8FAFC")));
		chart_->setBackgroundBrush(QBrush(QColor("#0B0E14")));
		chart_->legend()->hide();

		// X 轴
		QValueAxis *axis_x = new QValueAxis();
		axis_x->setRange(0, 20);
		axis_x->setTitleText("时间序列");
		axis_x->setTitleBrush(QBrush(QColor("#F8FAFC")));
		axis_x->setLabelsBrush(QBrush(QColor("#94A3B8")));
		axis_x->setGridLineColor(QColor("#1E293B"));
		chart_->addAxis(axis_x, Qt::AlignBottom);
		series_->attachAxis(axis_x);

		// Y 轴
		QValueAxis *axis_y = new QValueAxis();
		axis_y->setRange(0, 100);
		axis_y->setTitleText("数值");
		axis_y->setTitleBrush(QBrush(QColor("#F8FAFC")));
		axis_y->setLabelsBrush(QBrush(QColor("#94A3B8")));
		axis_y->setGridLineColor(QColor("#1E293B"));
		chart_->addAxis(axis_y, Qt::AlignLeft);
		series_->attachAxis(axis_y);

		chart_view_->setChart(chart_);
		chart_view_->setRenderHint(QPainter::Antialiasing);
	}

	void update_chart()
	{
		series_->clear();

		for (size_t i = 0; i < data_buffer_.size(); ++i)
		{
			series_->append(i, data_buffer_[i]);
		}

		// 动态调整 Y 轴范围
		if (!data_buffer_.empty())
		{
			int max_val = *std::max_element(data_buffer_.begin(), data_buffer_.end());
			int min_val = *std::min_element(data_buffer_.begin(), data_buffer_.end());

			int y_max = std::max(100, max_val + 10);
			int y_min = std::max(0, min_val - 10);

			dynamic_cast<QValueAxis *>(chart_->axes(Qt::Vertical).first())->setRange(y_min, y_max);
		}
	}

	// Socket 相关
	tools::Socket server_socket_;
	int client_fd_;

	// Qt 组件
	QTimer *timer_;
	QLabel *status_label_;
	QLabel *stats_label_;
	QChartView *chart_view_;
	QChart *chart_;
	QLineSeries *series_;

	// 数据缓冲区
	std::deque<int> data_buffer_;
};

#include "server.moc"

int main(int argc, char **argv)
{
	QApplication app(argc, argv);

	if (argc < 3)
	{
		qCritical() << "Usage: ./server <ip> <port>";
		return 1;
	}

	std::string ip = argv[1];
	int port = atoi(argv[2]);

	ServerWindow window(ip, port);
	window.show();

	return app.exec();
}
