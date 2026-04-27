import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, ScrollView } from "react-native";
import { useCharacterStore } from "../store/characterStore";
import { ROLE_PRESETS, KEYWORD_STAT_BONUSES } from "../constants/gameData";
import { GlassCard } from "../components/GlassCard";
import { User, Sword, Shield, Book, Zap } from "lucide-react-native";

export const CharacterCreation = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [selectedRole, setSelectedRole] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  
  const createCharacter = useCharacterStore((state) => state.createCharacter);
  const setStoreName = useCharacterStore((state) => state.setName);

  const roles = Object.keys(ROLE_PRESETS);
  const keywordOptions = Object.keys(KEYWORD_STAT_BONUSES);

  const handleCreate = () => {
    if (!name) return;
    setStoreName(name);
    createCharacter(age ? parseInt(age) : null, selectedRole, selectedKeywords);
  };

  const toggleKeyword = (kw: string) => {
    if (selectedKeywords.includes(kw)) {
      setSelectedKeywords(selectedKeywords.filter(k => k !== kw));
    } else {
      setSelectedKeywords([...selectedKeywords, kw]);
    }
  };

  return (
    <ScrollView className="flex-1 bg-slate-950 p-6 pt-12">
      <Text className="text-3xl font-bold text-white mb-6">Create Hero</Text>
      
      <GlassCard className="mb-6">
        <Text className="text-blue-400 font-bold mb-2 uppercase text-xs">Identity</Text>
        <TextInput
          className="bg-slate-900/50 text-white p-4 rounded-xl border border-slate-700 mb-4"
          placeholder="Hero Name"
          placeholderTextColor="#64748b"
          value={name}
          onChangeText={setName}
        />
        <TextInput
          className="bg-slate-900/50 text-white p-4 rounded-xl border border-slate-700"
          placeholder="Age (Optional)"
          placeholderTextColor="#64748b"
          keyboardType="numeric"
          value={age}
          onChangeText={setAge}
        />
      </GlassCard>

      <Text className="text-blue-400 font-bold mb-3 uppercase text-xs">Choose Role</Text>
      <View className="flex-row flex-wrap mb-6">
        {roles.map(role => (
          <TouchableOpacity
            key={role}
            onPress={() => setSelectedRole(role)}
            className={`mr-2 mb-2 px-4 py-2 rounded-full border ${
              selectedRole === role ? "bg-blue-600 border-blue-400" : "bg-slate-900/50 border-slate-700"
            }`}
          >
            <Text className={`capitalize font-medium ${selectedRole === role ? "text-white" : "text-slate-400"}`}>
              {role}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text className="text-blue-400 font-bold mb-3 uppercase text-xs">Keywords</Text>
      <View className="flex-row flex-wrap mb-10">
        {keywordOptions.map(kw => (
          <TouchableOpacity
            key={kw}
            onPress={() => toggleKeyword(kw)}
            className={`mr-2 mb-2 px-3 py-1.5 rounded-lg border ${
              selectedKeywords.includes(kw) ? "bg-purple-600 border-purple-400" : "bg-slate-900/50 border-slate-700"
            }`}
          >
            <Text className={`capitalize text-sm ${selectedKeywords.includes(kw) ? "text-white" : "text-slate-400"}`}>
              {kw}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        onPress={handleCreate}
        disabled={!name}
        className={`w-full py-5 rounded-2xl flex-row justify-center items-center ${
          name ? "bg-blue-600 shadow-lg shadow-blue-500/40" : "bg-slate-800"
        } mb-20`}
      >
        <Zap size={20} color="white" className="mr-2" />
        <Text className="text-white font-bold text-lg">Summon Hero</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};
