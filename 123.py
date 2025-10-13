from manager.group_state_manager import GroupStateManager

def test_group_state_manager():
    manager = GroupStateManager()

    # 初始化三個 timer
    timer1 = "timer1"
    timer2 = "timer2"
    timer3 = "timer3"
    group = "a"

    print("\n--- 初始狀態 ---")
    assert manager.can_select(group, timer1)
    manager.select(group, timer1)  # timer1 鎖定群組

    print("\n--- timer2 嘗試選擇（應該 idle）---")
    assert not manager.can_select(group, timer2)
    assert manager.is_idle(group, timer2)

    print("\n--- timer1 再次選擇（解除鎖定）---")
    manager.select(group, timer1)  # 解除鎖定

    print("\n--- timer2 再次嘗試選擇（應該成功）---")
    assert manager.can_select(group, timer2)
    manager.select(group, timer2)  # timer2 鎖定群組

    print("\n--- timer3 在不同群組（應該不受影響）---")
    assert manager.can_select("none", timer3)
    manager.select("none", timer3)

    print("\n✅ 測試完成，邏輯正確")

if __name__ == "__main__":
    test_group_state_manager()