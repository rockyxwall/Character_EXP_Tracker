import React, { useState } from "react";
import { View, Text, ScrollView, TouchableOpacity, FlatList } from "react-native";
import { useCharacterStore } from "../store/characterStore";
import { GlassCard } from "../components/GlassCard";
import { Swords, Skull, ChevronLeft } from "lucide-react-native";

const MONSTERS = [
  { id: "1", name: "Slime", level: 1, baseExp: 10 },
  { id: "2", name: "Horned Rabbit", level: 4, baseExp: 40 },
  { id: "3", name: "Goblin", level: 10, baseExp: 100 },
  { id: "4", name: "Orc", level: 25, baseExp: 500 },
  { id: "5", name: "Drake", level: 50, baseExp: 2500 },
];

export const Battle = ({ onBack }: { onBack: () => void }) => {
  const gainExp = useCharacterStore((state) => state.gainExp);
  const [battleLog, setBattleLog] = useState<string[]>([]);

  const handleBattle = (monsterName: string, level: number, qty: number) => {
    gainExp(level, qty);
    setBattleLog(prev => [`Fought ${qty}x ${monsterName} (Lv ${level})`, ...prev.slice(0, 4)]);
  };

  return (
    <View className="flex-1 bg-slate-950 p-6 pt-12">
      <View className="flex-row items-center mb-8">
        <TouchableOpacity onPress={onBack} className="mr-4">
          <ChevronLeft size={24} color="white" />
        </TouchableOpacity>
        <Text className="text-3xl font-bold text-white">Hunting Ground</Text>
      </View>

      <Text className="text-blue-400 font-bold mb-4 uppercase text-xs">Available Targets</Text>
      <ScrollView className="mb-6 flex-grow-0">
        {MONSTERS.map((m) => (
          <GlassCard key={m.id} className="mb-4">
            <View className="flex-row justify-between items-center">
              <View>
                <Text className="text-lg font-bold text-white">{m.name}</Text>
                <Text className="text-slate-400">Level {m.level}</Text>
              </View>
              <View className="flex-row">
                <TouchableOpacity 
                  onPress={() => handleBattle(m.name, m.level, 1)}
                  className="bg-blue-600 px-4 py-2 rounded-xl mr-2"
                >
                  <Text className="text-white font-bold">x1</Text>
                </TouchableOpacity>
                <TouchableOpacity 
                  onPress={() => handleBattle(m.name, m.level, 10)}
                  className="bg-indigo-600 px-4 py-2 rounded-xl"
                >
                  <Text className="text-white font-bold">x10</Text>
                </TouchableOpacity>
              </View>
            </View>
          </GlassCard>
        ))}
      </ScrollView>

      <Text className="text-red-400 font-bold mb-4 uppercase text-xs">Battle Log</Text>
      <GlassCard className="flex-1 bg-black/40">
        {battleLog.length === 0 ? (
          <Text className="text-slate-600 italic text-center py-10">No battles yet...</Text>
        ) : (
          battleLog.map((log, i) => (
            <View key={i} className="flex-row items-center mb-2">
              <Skull size={14} color="#f87171" className="mr-2" />
              <Text className="text-slate-300 text-sm">{log}</Text>
            </View>
          ))
        )}
      </GlassCard>
    </View>
  );
};
