#include <chrono>
#include <functional>
#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <opencv2/opencv.hpp>

class SchrodingerVisionNode : public rclcpp::Node {
public:
    SchrodingerVisionNode() : Node("schrodinger_vision_node") {
        vel_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);

        // ~60 Hz timer
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(16), 
            std::bind(&SchrodingerVisionNode::update_loop, this)
        );

        cap_.open(0);
        if (!cap_.isOpened()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open video capture device!");
        } else {
            RCLCPP_INFO(this->get_logger(), "Vision node initialized successfully.");
        }
    }

private:
    void update_loop() {
        cv::Mat frame;
        cap_ >> frame;
        if (frame.empty()) return;

        // TODO: ArUco detection + solvePnP pose estimation. Until then this publishes
        // a constant forward velocity and does not use the frame.
        geometry_msgs::msg::Twist twist_msg;
        twist_msg.linear.x = 0.5;  // constant placeholder command
        twist_msg.angular.z = 0.0;

        vel_pub_->publish(twist_msg);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    cv::VideoCapture cap_;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SchrodingerVisionNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
