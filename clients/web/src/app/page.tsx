"use client";

import React, { useState, useEffect } from "react";

interface ServiceStatus {
  name: string;
  port: number;
  url: string;
  uiUrl: string;
  status: "checking" | "online" | "offline";
  description: string;
  icon: string;
}

export default function MicroFrontendHub() {
  const [activeTab, setActiveTab] = useState<string>("overview");

  const [services, setServices] = useState<Record<string, ServiceStatus>>({
    ai: {
      name: "Module AI Chẩn Đoán & Phẩm Cấp",
      port: 8001,
      url: "http://localhost:8001",
      uiUrl: "http://localhost:8001/ui",
      status: "checking",
      description: "Nhận diện sâu bệnh (Task 3.2, 5.2) & Phân loại mít xuất khẩu (Task 6.2)",
      icon: "🔬"
    },
    recommendation: {
      name: "Module Khuyến Nông & Phác Đồ",
      port: 8002,
      url: "http://localhost:8002",
      uiUrl: "http://localhost:8002/ui",
      status: "checking",
      description: "Khuyến nghị phác đồ IPM kết hợp thời tiết & cảm biến (Task 6.1)",
      icon: "🌾"
    },
    core: {
      name: "Module Quản Lý Vườn & Bản Đồ Dịch Tễ",
      port: 8003,
      url: "http://localhost:8003",
      uiUrl: "http://localhost:8003/ui",
      status: "checking",
      description: "Theo dõi tình hình sâu bệnh vùng & dữ liệu nông hộ (Task 7.1, 7.2)",
      icon: "🗺️"
    },
    iot: {
      name: "Module IoT Gateway & Telemetry",
      port: 8004,
      url: "http://localhost:8004",
      uiUrl: "http://localhost:8004/ui",
      status: "checking",
      description: "Tiếp nhận luồng MQTT cảm biến vườn thời gian thực (Task 4.1, 7.2)",
      icon: "📡"
    }
  });

  // Kiểm tra sức khỏe từng service độc lập (Fault Isolation)
  useEffect(() => {
    const checkHealth = async () => {
      const updated = { ...services };
      for (const key of Object.keys(updated)) {
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 1500);
          const res = await fetch(`${updated[key].url}/health`, {
            signal: controller.signal,
            mode: "cors"
          });
          clearTimeout(timeoutId);
          updated[key].status = res.ok ? "online" : "offline";
        } catch {
          updated[key].status = "offline";
        }
      }
      setServices(updated);
    };

    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ fontFamily: "system-ui, -apple-system, sans-serif", minHeight: "100vh", backgroundColor: "#f8fafc", color: "#1e293b" }}>
      {/* Thanh Top Header chung của Hệ Thống */}
      <header style={{ backgroundColor: "#065f46", color: "white", padding: "16px 24px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "20px", fontWeight: "bold" }}>
            🍈 Smart Jackfruit AgriTech Platform - Micro-Frontend Portal
          </h1>
          <p style={{ margin: 0, fontSize: "12px", opacity: 0.85 }}>
            Kiến trúc Micro-Frontend: Các module hoạt động độc lập, không làm tê liệt lẫn nhau
          </p>
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          {Object.entries(services).map(([key, s]) => (
            <span
              key={key}
              title={`${s.name} (${s.url})`}
              style={{
                fontSize: "11px",
                padding: "3px 8px",
                borderRadius: "12px",
                backgroundColor: s.status === "online" ? "#059669" : "#dc2626",
                display: "inline-flex",
                alignItems: "center",
                gap: "4px"
              }}
            >
              <span>{s.icon}</span>
              <span>:{s.port}</span>
              <span>{s.status === "online" ? "●" : "○"}</span>
            </span>
          ))}
        </div>
      </header>

      {/* Thanh Menu điều hướng giữa các Module */}
      <nav style={{ backgroundColor: "white", borderBottom: "1px solid #e2e8f0", padding: "0 24px", display: "flex", gap: "12px" }}>
        <button
          onClick={() => setActiveTab("overview")}
          style={{
            padding: "12px 16px",
            border: "none",
            background: "none",
            cursor: "pointer",
            fontWeight: activeTab === "overview" ? "bold" : "normal",
            color: activeTab === "overview" ? "#065f46" : "#64748b",
            borderBottom: activeTab === "overview" ? "3px solid #065f46" : "3px solid transparent"
          }}
        >
          📊 Tổng Quan Hệ Thống
        </button>

        {Object.entries(services).map(([key, s]) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            style={{
              padding: "12px 16px",
              border: "none",
              background: "none",
              cursor: "pointer",
              fontWeight: activeTab === key ? "bold" : "normal",
              color: activeTab === key ? "#065f46" : "#64748b",
              borderBottom: activeTab === key ? "3px solid #065f46" : "3px solid transparent",
              display: "flex",
              alignItems: "center",
              gap: "6px"
            }}
          >
            <span>{s.icon}</span>
            <span>{s.name.split(" - ")[0]}</span>
          </button>
        ))}
      </nav>

      {/* Nội dung hiển thị theo Tab đã chọn */}
      <main style={{ padding: "24px", maxWidth: "1400px", margin: "0 auto" }}>
        {activeTab === "overview" && (
          <div>
            <div style={{ marginBottom: "24px" }}>
              <h2 style={{ fontSize: "22px", fontWeight: "bold" }}>Trung Tâm Điều Phối Các Module Độc Lập</h2>
              <p style={{ color: "#64748b", fontSize: "14px" }}>
                Mỗi module dưới đây có <b>UI độc lập riêng</b>, chạy trên tiến trình riêng. Nếu một module tắt hoặc gặp sự cố, các module khác vẫn phục vụ người dùng bình thường.
              </p>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "20px" }}>
              {Object.entries(services).map(([key, s]) => (
                <div
                  key={key}
                  style={{
                    backgroundColor: "white",
                    borderRadius: "12px",
                    border: "1px solid #e2e8f0",
                    padding: "20px",
                    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between"
                  }}
                >
                  <div>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                      <span style={{ fontSize: "32px" }}>{s.icon}</span>
                      <span
                        style={{
                          fontSize: "12px",
                          fontWeight: "bold",
                          padding: "2px 8px",
                          borderRadius: "12px",
                          backgroundColor: s.status === "online" ? "#dcfce7" : "#fee2e2",
                          color: s.status === "online" ? "#166534" : "#991b1b"
                        }}
                      >
                        {s.status === "online" ? "ĐANG HOẠT ĐỘNG" : "OFFLINE / CHỜ BẬT"}
                      </span>
                    </div>
                    <h3 style={{ fontSize: "17px", fontWeight: "bold", margin: "0 0 6px 0" }}>{s.name}</h3>
                    <p style={{ fontSize: "13px", color: "#64748b", margin: "0 0 16px 0", lineHeight: "1.4" }}>
                      {s.description}
                    </p>
                  </div>

                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      onClick={() => setActiveTab(key)}
                      style={{
                        flex: 1,
                        padding: "8px 12px",
                        backgroundColor: "#065f46",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        cursor: "pointer",
                        fontSize: "13px",
                        fontWeight: "500"
                      }}
                    >
                      Nhúng Trong Portal
                    </button>
                    <a
                      href={s.uiUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        padding: "8px 12px",
                        backgroundColor: "#f1f5f9",
                        color: "#334155",
                        borderRadius: "6px",
                        fontSize: "13px",
                        textDecoration: "none",
                        display: "flex",
                        alignItems: "center"
                      }}
                    >
                      Mở Tab Riêng ↗
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Khung nhúng Micro-Frontend độc lập qua iframe */}
        {activeTab !== "overview" && services[activeTab] && (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ fontSize: "24px" }}>{services[activeTab].icon}</span>
                <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0 }}>
                  {services[activeTab].name}
                </h2>
                <span style={{ fontSize: "12px", color: "#64748b" }}>
                  ({services[activeTab].uiUrl})
                </span>
              </div>
              <a
                href={services[activeTab].uiUrl}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  fontSize: "13px",
                  color: "#065f46",
                  textDecoration: "none",
                  fontWeight: "500"
                }}
              >
                Mở toàn màn hình ở tab riêng ↗
              </a>
            </div>

            <div style={{ backgroundColor: "white", borderRadius: "12px", border: "1px solid #cbd5e1", overflow: "hidden", minHeight: "750px", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.05)" }}>
              <iframe
                src={services[activeTab].uiUrl}
                title={services[activeTab].name}
                style={{ width: "100%", height: "750px", border: "none" }}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
