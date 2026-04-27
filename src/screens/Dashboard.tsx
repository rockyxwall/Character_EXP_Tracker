import React from "react";
import { View, Text, ScrollView, TouchableOpacity } from "react-native";
import { useCharacterStore } from "../store/characterStore";
import { GlassCard } from "../components/GlassCard";
import { STATS } from "../constants/gameData";
import { Sword, Zap, Brain, Shield, Wind, RefreshCcw } from "lucide-react-native";

const StatIcon = ({ name, color }: { name: string; color: string }) => {
  switch (name) {
    case "STR": return <Sword size={18} color={color} />;
    case "VIT": return <Shield size={18} color={color} />;
    case "AGI": return <Wind size={18} color={color} />;
    case "DEX": return <Zap size={18} color={color} />;
    case "MNA": return <Brain size={18} color={color} />;
    default: return null;
  }
};

export const Dashboard = () => {
  const { name, race, level, currentExp, expToNext, stats, reset } = useCharacterStore();
  const expProgress = (currentExp / expToNext) * 100;

  return (
    <ScrollView className="flex-1 bg-slate-950 p-6 pt-12">
      <View className="flex-row justify-between items-center mb-8">
        <View>
          <Text className="text-slate-400 text-sm font-medium uppercase tracking-widest">{race} Level {level}</Text>
          <Text className="text-3xl font-bold text-white">{name}</Text>
        </View>
        <TouchableOpacity onPress={reset} className="bg-slate-900 p-3 rounded-full border border-slate-800">
          <RefreshCcw size={20} color="#64748b" />
        </TouchableOpacity>
      </View>

      <GlassCard className="mb-6">
        <View className="flex-row justify-between mb-2">
          <Text className="text-slate-300 font-bold">EXP</Text>
          <Text className="text-blue-400 font-bold">{currentExp} / {expToNext}</Text>
        </View>
        <View className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
          <View 
            className="h-full bg-blue-500 rounded-full" 
            style={{ width: `${Math.min(100, expProgress)}%` }} 
          />
        </View>
      </GlassCard>

      <Text className="text-blue-400 font-bold mb-4 uppercase text-xs tracking-tighter">Attribute Matrix</Text>
      <View className="flex-row flex-wrap justify-between">
        {STATS.map((stat) => (
          <GlassCard key={stat} className="w-[48%] mb-4">
            <View className="flex-row items-center mb-1">
              <StatIcon name={stat} color="#60a5fa" />
              <Text className="text-slate-400 ml-2 font-bold text-xs">{stat}</Text>
            </View>
            <Text className="text-2xl font-bold text-white">{stats[stat]}</Text>
          </GlassCard>
        ))}
      </View>

      <TouchableOpacity 
        className="w-full bg-blue-600 py-4 rounded-2xl flex-row justify-center items-center mt-4 shadow-lg shadow-blue-500/30"
      >
        <Text className="text-white font-bold text-lg">Enter Battle Arena</Text>
      </TouchableOpacity>

      <View className="h-20" />
    </ScrollView>
  );
};
