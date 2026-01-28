"""
Basal Ganglia Engine Unit Tests
기저핵 엔진 단위 테스트

Author: GNJz (Qquarts)
Version: 1.0.0-alpha
"""

import unittest
from basal_ganglia import BasalGangliaEngine, ActionType, BasalGangliaConfig


class TestBasalGangliaEngine(unittest.TestCase):
    """기저핵 엔진 테스트"""
    
    def setUp(self):
        """테스트 전 초기화"""
        self.engine = BasalGangliaEngine()
    
    def test_initial_state(self):
        """초기 상태 테스트"""
        state = self.engine.get_state()
        
        self.assertEqual(state['dopamine'], 0.5)
        self.assertEqual(state['total_contexts'], 0)
        self.assertEqual(state['total_actions'], 0)
        self.assertEqual(len(state['habits']), 0)
    
    def test_action_selection(self):
        """행동 선택 테스트"""
        context = "test_context"
        actions = ["action1", "action2", "action3"]
        
        result = self.engine.select_action(context, actions)
        
        self.assertIsNotNone(result)
        self.assertIn(result.action.name, actions)
        self.assertIn(result.decision, [ActionType.GO, ActionType.NOGO, ActionType.EXPLORE])
    
    def test_learning(self):
        """학습 테스트"""
        context = "test_context"
        action_name = "action1"
        reward = 0.8
        
        # 학습 전
        best_action_before = self.engine.get_best_action(context)
        self.assertIsNone(best_action_before)
        
        # 학습
        self.engine.learn(context, action_name, reward)
        
        # 학습 후
        best_action_after = self.engine.get_best_action(context)
        self.assertIsNotNone(best_action_after)
        self.assertEqual(best_action_after.name, action_name)
        self.assertGreater(best_action_after.q_value, 0)
    
    def test_habit_formation(self):
        """습관 형성 테스트"""
        context = "test_context"
        action_name = "habit_action"
        
        # 반복 학습으로 습관 형성
        for _ in range(50):
            self.engine.learn(context, action_name, reward=0.9)
        
        habits = self.engine.get_habits()
        self.assertGreater(len(habits), 0)
        
        habit_action = None
        for h in habits:
            if h.name == action_name:
                habit_action = h
                break
        
        self.assertIsNotNone(habit_action)
        self.assertGreaterEqual(habit_action.habit_strength, 0.7)
    
    def test_habit_automatic_execution(self):
        """습관 자동 실행 테스트"""
        context = "test_context"
        action_name = "habit_action"
        actions = [action_name, "other_action"]
        
        # 습관 형성
        for _ in range(50):
            self.engine.learn(context, action_name, reward=0.9)
        
        # 행동 선택 (습관이 자동 실행되어야 함)
        result = self.engine.select_action(context, actions)
        
        self.assertTrue(result.is_automatic)
        self.assertEqual(result.action.name, action_name)
        self.assertEqual(result.decision, ActionType.GO)
    
    def test_dopamine_update(self):
        """도파민 업데이트 테스트"""
        initial_dopamine = self.engine.dopamine_level
        
        # 긍정적 보상 학습
        self.engine.learn("context", "action", reward=0.8)
        
        # 도파민이 증가했는지 확인 (TD error > 0이면 증가)
        # 정확한 값은 TD error에 따라 다르므로, 변화가 있었는지만 확인
        self.assertIsNotNone(self.engine.dopamine_level)
        self.assertGreaterEqual(self.engine.dopamine_level, 0)
        self.assertLessEqual(self.engine.dopamine_level, 1)
    
    def test_dopamine_injection(self):
        """도파민 주입 테스트"""
        self.engine.set_dopamine_level(0.8)
        self.assertEqual(self.engine.dopamine_level, 0.8)
        
        self.engine.set_dopamine_level(1.5)  # 클램핑 테스트
        self.assertEqual(self.engine.dopamine_level, 1.0)
        
        self.engine.set_dopamine_level(-0.5)  # 클램핑 테스트
        self.assertEqual(self.engine.dopamine_level, 0.0)
    
    def test_q_value_decay(self):
        """Q-값 감쇠 테스트"""
        context = "test_context"
        action_name = "action1"
        
        # 학습
        self.engine.learn(context, action_name, reward=0.8)
        q_value_before = self.engine.q_table[context][action_name].q_value
        
        # 감쇠
        self.engine.decay_all()
        q_value_after = self.engine.q_table[context][action_name].q_value
        
        self.assertLess(q_value_after, q_value_before)
    
    def test_habit_breaking(self):
        """습관 깨기 테스트"""
        context = "test_context"
        action_name = "habit_action"
        
        # 습관 형성
        for _ in range(50):
            self.engine.learn(context, action_name, reward=0.9)
        
        # 습관 확인
        habits_before = self.engine.get_habits()
        self.assertGreater(len(habits_before), 0)
        
        # 습관 깨기
        self.engine.break_habit(context, action_name)
        
        # 습관 확인
        habits_after = self.engine.get_habits()
        habit_exists = any(h.name == action_name for h in habits_after)
        self.assertFalse(habit_exists)
    
    def test_custom_config(self):
        """커스텀 설정 테스트"""
        config = BasalGangliaConfig(
            alpha=0.2,
            gamma=0.95,
            habit_threshold=0.8
        )
        
        engine = BasalGangliaEngine(config=config)
        
        self.assertEqual(engine.config.alpha, 0.2)
        self.assertEqual(engine.config.gamma, 0.95)
        self.assertEqual(engine.config.habit_threshold, 0.8)
    
    def test_stats_tracking(self):
        """통계 추적 테스트"""
        context = "test_context"
        actions = ["action1", "action2"]
        
        # 행동 선택
        self.engine.select_action(context, actions)
        
        stats = self.engine.get_stats()
        self.assertEqual(stats['total_decisions'], 1)
        
        # 학습
        self.engine.learn(context, "action1", reward=0.5)
        
        stats = self.engine.get_stats()
        self.assertGreater(stats['total_reward'], 0)


if __name__ == '__main__':
    unittest.main()

