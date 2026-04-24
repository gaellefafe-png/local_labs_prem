# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict
import io

st.set_page_config(layout="wide", page_title="Генетические алгоритмы", page_icon="🧬")


# ============================================================
# БЛОК ЗАДАНИЯ №1 (базовое) - Поиск экстремума функции
# ============================================================

class Task1GA:
    def __init__(self, variant: int):
        self.variant = variant
        self.set_params_by_variant()
        self.MAX_INT = 2 ** self.chromosome_length - 1

    def set_params_by_variant(self):
        """Установка параметров по варианту (таблица 1, область [-5;5])"""
        variants_5 = {
            1: {"func": lambda x: 2 * x - 3.3 * x * math.cos(9.3 * x) - 2.3 * math.sin(1.7 * x),
                "extreme": "min", "coding": "binary", "pc": 0.9, "pm": 0.2,
                "parent_select": "tournament", "reduction": "tournament"},
            2: {"func": lambda x: math.exp(-0.5 * x ** 2) * (1 if math.cos(9.3 * x - 1) > 0 else -1),
                "extreme": "min", "coding": "gray", "pc": 0.9, "pm": 0.1,
                "parent_select": "random", "reduction": "roulette"},
            3: {"func": lambda x: -0.6 * x + 5.3 * abs(math.cos(6.1 * x)) * math.cos(3.6 * x),
                "extreme": "min", "coding": "binary", "pc": 0.8, "pm": 0.2,
                "parent_select": "random", "reduction": "tournament"},
            4: {"func": lambda x: -1.3 * math.sin(1.6 * x ** 2 - 0.3) * math.exp(-0.3 * x + 0.5),
                "extreme": "max", "coding": "gray", "pc": 0.85, "pm": 0.15,
                "parent_select": "best_with_best", "reduction": "roulette"},
            5: {"func": lambda x: 0.9 * abs(math.sin(3.7 * x)) * math.cos(6.1 * x),
                "extreme": "max", "coding": "binary", "pc": 0.9, "pm": 0.15,
                "parent_select": "random", "reduction": "tournament"},
            6: {"func": lambda x: 0.8 * x + 1.4 * math.cos(1.8 * x ** 2) * math.exp(0.4 * x),
                "extreme": "min", "coding": "gray", "pc": 0.85, "pm": 0.1,
                "parent_select": "best_with_best", "reduction": "roulette"},
            7: {"func": lambda x: -math.sin(0.9 * x - 1) - math.sin(1.8 * x - 1) * math.cos(7.8 * x),
                "extreme": "max", "coding": "binary", "pc": 0.8, "pm": 0.15,
                "parent_select": "best_with_best", "reduction": "tournament"},
            8: {"func": lambda x: 0.8 * x + 1.1 * x * math.sin(9.3 * x) - 0.7 * math.cos(0.8 * x),
                "extreme": "min", "coding": "gray", "pc": 0.9, "pm": 0.1,
                "parent_select": "random", "reduction": "roulette"},
            9: {"func": lambda x: 0.2 * x - 1.1 * math.exp(-0.4 * x ** 2) * (1 if math.cos(9.5 * x + 1.5) > 0 else -1),
                "extreme": "min", "coding": "binary", "pc": 0.85, "pm": 0.15,
                "parent_select": "best_with_best", "reduction": "tournament"},
            10: {"func": lambda x: 0.3 * x + x * math.cos(7.3 * x) - 0.7 * math.sin(1.3 * x),
                 "extreme": "max", "coding": "gray", "pc": 0.8, "pm": 0.2,
                 "parent_select": "random", "reduction": "roulette"},
        }

        # Варианты для области [-1;1] (11-16)
        variants_1 = {
            11: {"func": lambda x: 5.1 * abs(math.cos(15 * x)) * math.cos(33 * x),
                 "extreme": "max", "coding": "binary", "pc": 0.85, "pm": 0.15,
                 "parent_select": "random", "reduction": "roulette", "x_min": -1, "x_max": 1},
            12: {"func": lambda x: 3.5 * x + math.sin(47 * x ** 2 + 2) - 6 * (x ** 2),
                 "extreme": "max", "coding": "gray", "pc": 0.8, "pm": 0.1,
                 "parent_select": "best_with_best", "reduction": "tournament", "x_min": -1, "x_max": 1},
            13: {"func": lambda x: 9 * x - 9.7 * abs(math.sin(37 * x)) * math.cos(27 * x),
                 "extreme": "min", "coding": "binary", "pc": 0.9, "pm": 0.2,
                 "parent_select": "random", "reduction": "roulette", "x_min": -1, "x_max": 1},
            14: {"func": lambda x: 3.1 * x - 3 * math.sin(31.4 * x ** 2 + 7) - 6 * (x ** 2),
                 "extreme": "max", "coding": "gray", "pc": 0.85, "pm": 0.2,
                 "parent_select": "random", "reduction": "tournament", "x_min": -1, "x_max": 1},
            15: {"func": lambda x: 6.9 * x + 7.5 * abs(math.cos(39 * x)) * math.cos(31 * x),
                 "extreme": "max", "coding": "binary", "pc": 0.8, "pm": 0.1,
                 "parent_select": "random", "reduction": "roulette", "x_min": -1, "x_max": 1},
            16: {"func": lambda x: 0.7 * x + 1.4 * x * math.sin(43 * x) - 2.3 * math.cos(5.4 * x),
                 "extreme": "max", "coding": "gray", "pc": 0.9, "pm": 0.15,
                 "parent_select": "best_with_best", "reduction": "tournament", "x_min": -1, "x_max": 1},
        }

        # Варианты для области [-3;3] (17-23)
        variants_3 = {
            17: {"func": lambda x: math.cos(1.2 * x - 2) - math.cos(1.7 * x - 1) * math.sin(8.4 * x),
                 "extreme": "max", "coding": "binary", "pc": 0.85, "pm": 0.15,
                 "parent_select": "random", "reduction": "roulette", "x_min": -3, "x_max": 3},
            18: {"func": lambda x: -0.35 * x + 1.2 * math.sin(2.5 * x ** 2) * math.exp(0.3 * x),
                 "extreme": "max", "coding": "gray", "pc": 0.9, "pm": 0.1,
                 "parent_select": "best_with_best", "reduction": "tournament", "x_min": -3, "x_max": 3},
            19: {"func": lambda x: -0.5 * x - 0.7 * x * math.cos(9.2 * x + 3) + 0.9 * math.sin(0.9 * x - 1),
                 "extreme": "min", "coding": "binary", "pc": 0.8, "pm": 0.2,
                 "parent_select": "random", "reduction": "roulette", "x_min": -3, "x_max": 3},
            20: {"func": lambda x: -0.9 * abs(math.cos(4.1 * x)) * math.sin(6.8 * x),
                 "extreme": "min", "coding": "gray", "pc": 0.85, "pm": 0.15,
                 "parent_select": "random", "reduction": "tournament", "x_min": -3, "x_max": 3},
            21: {
                "func": lambda x: -0.5 * x + 1.2 * math.exp(-0.5 * x ** 2) * (1 if math.sin(9.7 * x + 1.3) > 0 else -1),
                "extreme": "max", "coding": "binary", "pc": 0.8, "pm": 0.1,
                "parent_select": "best_with_best", "reduction": "roulette", "x_min": -3, "x_max": 3},
            22: {"func": lambda x: -0.9 * x + 1.5 * math.cos(2.3 * x ** 2 - 0.5) * math.exp(-0.4 * x + 0.3),
                 "extreme": "min", "coding": "gray", "pc": 0.9, "pm": 0.15,
                 "parent_select": "random", "reduction": "tournament", "x_min": -3, "x_max": 3},
            23: {"func": lambda x: 0.2 * x + x * math.sin(8.9 * x) + 0.9 * math.cos(1.5 * x - 2),
                 "extreme": "min", "coding": "binary", "pc": 0.85, "pm": 0.15,
                 "parent_select": "random", "reduction": "roulette", "x_min": -3, "x_max": 3},
        }

        # Определяем область поиска по варианту
        if 1 <= self.variant <= 10:
            self.x_min, self.x_max = -5, 5
            params = variants_5.get(self.variant)
        elif 11 <= self.variant <= 16:
            self.x_min, self.x_max = -1, 1
            params = variants_1.get(self.variant)
        elif 17 <= self.variant <= 23:
            self.x_min, self.x_max = -3, 3
            params = variants_3.get(self.variant)
        else:
            raise ValueError(f"Неверный вариант: {self.variant}")

        if params is None:
            raise ValueError(f"Вариант {self.variant} не найден")

        self.target_func = params["func"]
        self.extreme = params["extreme"]
        self.coding = params["coding"]
        self.pc = params["pc"]
        self.pm = params["pm"]
        self.parent_select = params["parent_select"]
        self.reduction = params["reduction"]

        # Общие параметры
        self.population_size = 50
        self.chromosome_length = 20
        self.generations = 30
        self.tournament_size = 3

    def int_to_binary(self, value: int) -> str:
        return format(value, f'0{self.chromosome_length}b')

    def binary_to_int(self, binary: str) -> int:
        return int(binary, 2)

    def gray_to_binary(self, gray: str) -> str:
        binary = gray[0]
        for i in range(1, len(gray)):
            binary += str(int(binary[i - 1]) ^ int(gray[i]))
        return binary

    def binary_to_gray(self, binary: str) -> str:
        gray = binary[0]
        for i in range(1, len(binary)):
            gray += str(int(binary[i - 1]) ^ int(binary[i]))
        return gray

    def code(self, value: int) -> str:
        binary = self.int_to_binary(value)
        if self.coding == "gray":
            return self.binary_to_gray(binary)
        return binary

    def decode(self, chromosome: str) -> int:
        if self.coding == "gray":
            binary = self.gray_to_binary(chromosome)
            return self.binary_to_int(binary)
        return self.binary_to_int(chromosome)

    def int_to_x(self, value: int) -> float:
        max_int = self.MAX_INT
        return self.x_min + value * (self.x_max - self.x_min) / max_int

    def get_fitness_shift(self) -> float:
        xs = np.linspace(self.x_min, self.x_max, 5000)
        ys = [self.target_func(x) for x in xs]
        if self.extreme == "min":
            return max(ys)
        else:
            return abs(min(ys))

    def fitness(self, x: float) -> float:
        f_val = self.target_func(x)
        if self.extreme == "min":
            return self.fitness_shift - f_val + 1e-9
        else:
            return f_val - self.fitness_shift + 1e-9

    @dataclass
    class Individual:
        chromosome: str
        parent_ref: 'Task1GA' = None

        @property
        def x(self) -> float:
            return self.parent_ref.int_to_x(self.parent_ref.decode(self.chromosome))

        @property
        def f(self) -> float:
            return self.parent_ref.target_func(self.x)

        @property
        def fitness(self) -> float:
            return self.parent_ref.fitness(self.x)

    def generate_random_individual(self):
        value = random.randint(0, self.MAX_INT)
        chromosome = self.code(value)
        ind = self.Individual(chromosome)
        ind.parent_ref = self
        return ind

    def generate_initial_population(self):
        return [self.generate_random_individual() for _ in range(self.population_size)]

    def form_parent_pairs(self, population):
        if self.parent_select == "random":
            shuffled = population[:]
            random.shuffle(shuffled)
            pairs = []
            for i in range(0, len(shuffled) - 1, 2):
                pairs.append((shuffled[i], shuffled[i + 1]))
            return pairs
        elif self.parent_select == "best_with_best":
            sorted_pop = sorted(population, key=lambda ind: ind.fitness, reverse=True)
            pairs = []
            for i in range(0, len(sorted_pop) - 1, 2):
                pairs.append((sorted_pop[i], sorted_pop[i + 1]))
            random.shuffle(pairs)
            return pairs
        elif self.parent_select == "tournament":
            pairs = []
            for _ in range(self.population_size // 2):
                p1 = self.tournament_select(population)
                p2 = self.tournament_select(population)
                pairs.append((p1, p2))
            return pairs
        return []

    def tournament_select(self, population):
        tournament = random.sample(population, self.tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)

    def crossover(self, p1, p2):
        if random.random() > self.pc:
            return self.Individual(p1.chromosome, self), self.Individual(p2.chromosome, self)
        point = random.randint(1, self.chromosome_length - 1)
        c1 = p1.chromosome[:point] + p2.chromosome[point:]
        c2 = p2.chromosome[:point] + p1.chromosome[point:]
        return self.Individual(c1, self), self.Individual(c2, self)

    def mutate(self, individual):
        if random.random() > self.pm:
            return individual
        chrom = list(individual.chromosome)
        bit = random.randint(0, self.chromosome_length - 1)
        chrom[bit] = '1' if chrom[bit] == '0' else '0'
        return self.Individual(''.join(chrom), self)

    def reduction_tournament(self, population, offspring):
        candidates = population + offspring
        new_pop = []
        for _ in range(self.population_size):
            new_pop.append(self.tournament_select(candidates))
        return new_pop

    def reduction_roulette(self, population, offspring):
        candidates = population + offspring
        fitness_sum = sum(ind.fitness for ind in candidates)
        if fitness_sum <= 0:
            return random.sample(candidates, self.population_size)
        probs = [ind.fitness / fitness_sum for ind in candidates]
        indices = np.random.choice(len(candidates), size=self.population_size, replace=True, p=probs)
        return [candidates[i] for i in indices]

    def run(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)

        self.fitness_shift = self.get_fitness_shift()

        population = self.generate_initial_population()
        populations = {0: population[:]}
        avg_fitness_history = [sum(ind.fitness for ind in population) / self.population_size]

        for gen in range(1, self.generations + 1):
            parent_pairs = self.form_parent_pairs(population)
            offspring = []
            for p1, p2 in parent_pairs:
                c1, c2 = self.crossover(p1, p2)
                c1 = self.mutate(c1)
                c2 = self.mutate(c2)
                offspring.extend([c1, c2])

            if self.reduction == "tournament":
                population = self.reduction_tournament(population, offspring)
            else:
                population = self.reduction_roulette(population, offspring)

            if gen == 3:
                populations[3] = population[:]
            if gen == self.generations:
                populations[self.generations] = population[:]

            avg_fitness_history.append(sum(ind.fitness for ind in population) / self.population_size)

        return populations, avg_fitness_history


# ============================================================
# БЛОК ЗАДАНИЯ №2 (дополнительное) - Поиск бинарных КП
# ============================================================

class Task2GA:
    def __init__(self, variant: int):
        self.variant = variant
        self.set_params_by_variant()

    def set_params_by_variant(self):
        variants = {
            1: {"n": 25, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.85, "pm": 0.15,
                "parent_select": "random", "selection": "roulette"},
            2: {"n": 27, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.9, "pm": 0.15,
                "parent_select": "random", "selection": "tournament"},
            3: {"n": 29, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.8, "pm": 0.1,
                "parent_select": "best_with_best", "selection": "roulette"},
            4: {"n": 31, "population_size": 70, "psl_limit": 2, "k": 4, "pk": 0.85, "pm": 0.15,
                "parent_select": "best_with_best", "selection": "tournament"},
            5: {"n": 33, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.9, "pm": 0.2,
                "parent_select": "random", "selection": "roulette"},
            6: {"n": 35, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.8, "pm": 0.2,
                "parent_select": "best_with_best", "selection": "roulette"},
            7: {"n": 37, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.9, "pm": 0.1,
                "parent_select": "random", "selection": "tournament"},
            8: {"n": 39, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.85, "pm": 0.15,
                "parent_select": "random", "selection": "roulette"},
            9: {"n": 26, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.8, "pm": 0.15,
                "parent_select": "random", "selection": "tournament"},
            10: {"n": 28, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.85, "pm": 0.15,
                 "parent_select": "random", "selection": "roulette"},
            11: {"n": 30, "population_size": 50, "psl_limit": 2, "k": 4, "pk": 0.9, "pm": 0.1,
                 "parent_select": "best_with_best", "selection": "tournament"},
            12: {"n": 32, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.8, "pm": 0.2,
                 "parent_select": "random", "selection": "roulette"},
            13: {"n": 34, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.8, "pm": 0.1,
                 "parent_select": "best_with_best", "selection": "roulette"},
            14: {"n": 36, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.9, "pm": 0.15,
                 "parent_select": "random", "selection": "tournament"},
            15: {"n": 38, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.85, "pm": 0.15,
                 "parent_select": "random", "selection": "roulette"},
            16: {"n": 29, "population_size": 60, "psl_limit": 2, "k": 4, "pk": 0.9, "pm": 0.2,
                 "parent_select": "random", "selection": "tournament"},
            17: {"n": 31, "population_size": 70, "psl_limit": 2, "k": 4, "pk": 0.8, "pm": 0.1,
                 "parent_select": "random", "selection": "roulette"},
            18: {"n": 33, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.8, "pm": 0.15,
                 "parent_select": "best_with_best", "selection": "tournament"},
            19: {"n": 35, "population_size": 70, "psl_limit": 3, "k": 3, "pk": 0.9, "pm": 0.15,
                 "parent_select": "random", "selection": "tournament"},
            20: {"n": 37, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.8, "pm": 0.2,
                 "parent_select": "best_with_best", "selection": "roulette"},
            21: {"n": 39, "population_size": 70, "psl_limit": 4, "k": 3, "pk": 0.9, "pm": 0.2,
                 "parent_select": "best_with_best", "selection": "tournament"},
            22: {"n": 31, "population_size": 100, "psl_limit": 2, "k": 5, "pk": 0.85, "pm": 0.15,
                 "parent_select": "random", "selection": "roulette"},
            23: {"n": 35, "population_size": 100, "psl_limit": 3, "k": 4, "pk": 0.9, "pm": 0.2,
                 "parent_select": "best_with_best", "selection": "tournament"},
        }

        params = variants.get(self.variant)
        if params is None:
            raise ValueError(f"Вариант {self.variant} не найден")

        self.n = params["n"]
        self.population_size = params["population_size"]
        self.psl_limit = params["psl_limit"]
        self.k = params["k"]
        self.pk = params["pk"]
        self.pm = params["pm"]
        self.parent_select = params["parent_select"]
        self.selection = params["selection"]
        self.generations = 200
        self.elite_size = 2

    @dataclass
    class Individual:
        genes: List[int]

        @property
        def sequence_str(self) -> str:
            return "".join("+" if g == 1 else "-" for g in self.genes)

    def aperiodic_acf(self, sequence: List[int]):
        """Вычисление апериодической АКФ"""
        seq = np.array(sequence, dtype=int)
        n = len(seq)

        # Вычисляем АКФ для положительных сдвигов
        acf_positive = []
        for k in range(n):
            if k == 0:
                acf_positive.append(n)
            else:
                val = np.sum(seq[:n - k] * seq[k:])
                acf_positive.append(val)

        # АКФ симметрична
        acf_negative = acf_positive[1:][::-1]
        shifts = list(range(-(n - 1), n))
        values = acf_negative + acf_positive

        return shifts, values

    def positive_sidelobe_level(self, sequence: List[int]) -> int:
        """PSL = максимальный положительный боковой лепесток АКФ"""
        _, acf_vals = self.aperiodic_acf(sequence)
        center = self.n - 1
        sidelobes = [acf_vals[i] for i in range(len(acf_vals)) if i != center]
        positive = [v for v in sidelobes if v > 0]
        return max(positive) if positive else 0

    def fitness(self, sequence: List[int]) -> float:
        """FFn = N / PSL"""
        psl = self.positive_sidelobe_level(sequence)
        if psl == 0:
            return self.n * 10.0
        return self.n / psl

    def generate_random_individual(self):
        genes = [random.choice([-1, 1]) for _ in range(self.n)]
        return self.Individual(genes)

    def generate_initial_population(self):
        return [self.generate_random_individual() for _ in range(self.population_size)]

    def form_parent_pairs(self, population):
        if self.parent_select == "random":
            shuffled = population[:]
            random.shuffle(shuffled)
            pairs = []
            for i in range(0, len(shuffled) - 1, 2):
                pairs.append((shuffled[i], shuffled[i + 1]))
            return pairs
        else:  # best_with_best
            sorted_pop = sorted(population, key=lambda ind: self.fitness(ind.genes), reverse=True)
            pairs = []
            for i in range(0, len(sorted_pop) - 1, 2):
                pairs.append((sorted_pop[i], sorted_pop[i + 1]))
            random.shuffle(pairs)
            return pairs

    def crossover_one_point(self, p1, p2):
        if random.random() > self.pk:
            return self.Individual(p1.genes[:]), self.Individual(p2.genes[:])
        point = random.randint(1, self.n - 1)
        c1 = p1.genes[:point] + p2.genes[point:]
        c2 = p2.genes[:point] + p1.genes[point:]
        return self.Individual(c1), self.Individual(c2)

    def mutation_inversion(self, individual):
        if random.random() > self.pm:
            return individual
        genes = individual.genes[:]
        idx = random.randint(0, self.n - 1)
        genes[idx] *= -1
        return self.Individual(genes)

    def selection_roulette_with_elite(self, candidates):
        sorted_candidates = sorted(candidates, key=lambda ind: self.fitness(ind.genes), reverse=True)
        elite = sorted_candidates[:self.elite_size]

        rest = candidates
        rest_size = self.population_size - self.elite_size

        fitness_vals = [self.fitness(ind.genes) for ind in rest]
        total = sum(fitness_vals)
        if total <= 0:
            probs = [1 / len(rest)] * len(rest)
        else:
            probs = [f / total for f in fitness_vals]

        indices = np.random.choice(len(rest), size=rest_size, replace=True, p=probs)
        selected = [rest[i] for i in indices]

        return elite + selected

    def selection_tournament(self, candidates, tournament_size=3):
        new_pop = []
        candidates_list = list(candidates)
        for _ in range(self.population_size):
            tournament = random.sample(candidates_list, min(tournament_size, len(candidates_list)))
            winner = max(tournament, key=lambda ind: self.fitness(ind.genes))
            new_pop.append(self.Individual(winner.genes[:]))
        return new_pop

    def run(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)

        population = self.generate_initial_population()
        populations = {0: population[:]}
        avg_fitness_history = [sum(self.fitness(ind.genes) for ind in population) / self.population_size]
        best_psl_history = [
            self.positive_sidelobe_level(max(population, key=lambda ind: self.fitness(ind.genes)).genes)]

        found_sequences = {}

        for gen in range(1, self.generations + 1):
            parent_pairs = self.form_parent_pairs(population)
            offspring = []
            for p1, p2 in parent_pairs:
                c1, c2 = self.crossover_one_point(p1, p2)
                c1 = self.mutation_inversion(c1)
                c2 = self.mutation_inversion(c2)
                offspring.extend([c1, c2])

            # Добиваем до нужного размера
            while len(offspring) < self.population_size:
                offspring.append(self.generate_random_individual())

            candidates = population + offspring
            if self.selection == "roulette":
                population = self.selection_roulette_with_elite(candidates)
            else:
                population = self.selection_tournament(candidates)

            if gen == 3:
                populations[3] = population[:]
            if gen == self.generations:
                populations[self.generations] = population[:]

            avg_fitness_history.append(sum(self.fitness(ind.genes) for ind in population) / self.population_size)
            best_ind = max(population, key=lambda ind: self.fitness(ind.genes))
            best_psl_history.append(self.positive_sidelobe_level(best_ind.genes))

            # Сохраняем найденные последовательности
            for ind in population:
                psl = self.positive_sidelobe_level(ind.genes)
                if psl <= self.psl_limit:
                    key = ind.sequence_str
                    if key not in found_sequences:
                        found_sequences[key] = ind

        # Сортируем найденные по качеству
        found_list = list(found_sequences.values())
        found_list.sort(key=lambda ind: self.positive_sidelobe_level(ind.genes))

        return populations, avg_fitness_history, best_psl_history, found_list[:self.k]


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("🧬 Генетические алгоритмы")
st.markdown("Автоматизированное решение заданий по генетическим алгоритмам")

task = st.sidebar.radio("Выберите задание", ["Задание №1 (Поиск экстремума)", "Задание №2 (Поиск КП)"])

if task == "Задание №1 (Поиск экстремума)":
    st.header("📈 Задание №1: Поиск экстремума целевой функции")

    variant_options = list(range(1, 24))
    variant = st.selectbox("Выберите вариант (1-23)", variant_options, format_func=lambda x: f"Вариант {x}")

    generations = st.slider("Количество поколений", 10, 100, 30)
    seed = st.number_input("Seed (для воспроизводимости)", value=42, step=1)

    if st.button("🚀 Запустить ГА", type="primary"):
        with st.spinner("Выполняется генетический алгоритм..."):
            ga = Task1GA(variant)
            ga.generations = generations
            populations, avg_fitness = ga.run(seed=seed)

        st.success("Выполнено!")

        # ===== ВЫВОД НАЧАЛЬНЫХ ДАННЫХ =====
        st.subheader("📋 Начальные данные")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Вариант", variant)
        with col2:
            st.metric("Область поиска", f"[{ga.x_min}; {ga.x_max}]")
        with col3:
            st.metric("Экстремум", "Минимум" if ga.extreme == "min" else "Максимум")
        with col4:
            st.metric("Кодирование", "Двоичный код" if ga.coding == "binary" else "Код Грея")

        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.metric("Размер популяции", ga.population_size)
        with col6:
            st.metric("Длина хромосомы", f"{ga.chromosome_length} бит")
        with col7:
            st.metric("Pc (скрещивание)", f"{ga.pc}")
        with col8:
            st.metric("Pm (мутация)", f"{ga.pm}")

        st.markdown(f"**Формирование родительских пар:** {ga.parent_select}")
        st.markdown(f"**Редукция:** {ga.reduction}")

        # ===== ГРАФИК ЦЕЛЕВОЙ ФУНКЦИИ =====
        st.subheader("📈 График целевой функции")
        xs = np.linspace(ga.x_min, ga.x_max, 2000)
        ys = [ga.target_func(x) for x in xs]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(xs, ys, label='f(x)', linewidth=1.5)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Целевая функция (Вариант {variant})')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

        # ===== ГРАФИК ФУНКЦИИ ПРИСПОСОБЛЕННОСТИ =====
        st.subheader("📊 График функции приспособленности")
        fitness_ys = [ga.fitness(x) for x in xs]

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(xs, fitness_ys, color='green', linewidth=1.5)
        ax2.set_xlabel('x')
        ax2.set_ylabel('F(x)')
        ax2.set_title('Функция приспособленности')
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)

        # ===== ГРАФИКИ ПОПУЛЯЦИЙ =====
        st.subheader("👥 Визуализация популяций")

        pop_indices = [0, 3, generations] if generations >= 3 else [0, generations]

        for pop_idx in pop_indices:
            if pop_idx in populations:
                population = populations[pop_idx]

                fig3, ax3 = plt.subplots(figsize=(10, 5))
                ax3.plot(xs, ys, label='f(x)', linewidth=1.5, alpha=0.7)

                pop_x = [ind.x for ind in population]
                pop_f = [ind.f for ind in population]
                ax3.scatter(pop_x, pop_f, c='red', s=40, alpha=0.7, label='Особи популяции', zorder=5)

                ax3.set_xlabel('x')
                ax3.set_ylabel('f(x)')
                ax3.set_title(f'Популяция на графике целевой функции (поколение {pop_idx})')
                ax3.legend()
                ax3.grid(True, alpha=0.3)
                st.pyplot(fig3)

        # ===== ТАБЛИЦЫ ПОПУЛЯЦИЙ =====
        st.subheader("📋 Таблицы популяций")


        def display_population_table(population, ga_obj, title, pop_num):
            """Вывод таблицы: первые 10 и последние 10 особей"""
            st.markdown(f"**{title} (поколение {pop_num})**")

            # Первые 10
            st.caption("📌 Первые 10 особей")
            data_first = []
            for i, ind in enumerate(population[:10], 1):
                data_first.append({
                    "№": i,
                    "x": f"{ind.x:.8f}",
                    "Хромосома": ind.chromosome,
                    "f(x)": f"{ind.f:.8f}",
                    "F(x)": f"{ind.fitness:.8f}"
                })
            st.dataframe(data_first, use_container_width=True)

            # Последние 10
            if len(population) > 10:
                st.caption("📌 Последние 10 особей")
                data_last = []
                start_idx = len(population) - 10
                for i, ind in enumerate(population[start_idx:], start_idx + 1):
                    data_last.append({
                        "№": i,
                        "x": f"{ind.x:.8f}",
                        "Хромосома": ind.chromosome,
                        "f(x)": f"{ind.f:.8f}",
                        "F(x)": f"{ind.fitness:.8f}"
                    })
                st.dataframe(data_last, use_container_width=True)

            avg_f = sum(ind.fitness for ind in population) / len(population)
            st.caption(f"📊 Средняя приспособленность: {avg_f:.8f}")
            st.markdown("---")


        # Выводим таблицы для 0, 3 и последней популяции
        if 0 in populations:
            display_population_table(populations[0], ga, "НАЧАЛЬНАЯ ПОПУЛЯЦИЯ", 0)

        if 3 in populations:
            display_population_table(populations[3], ga, "ТРЕТЬЯ ПОПУЛЯЦИЯ", 3)
        elif generations < 3 and generations in populations:
            display_population_table(populations[generations], ga, f"ПОПУЛЯЦИЯ (поколение {generations})", generations)

        if generations in populations and generations != 0 and generations != 3:
            display_population_table(populations[generations], ga, "ПОСЛЕДНЯЯ ПОПУЛЯЦИЯ", generations)

        # ===== ГРАФИК СРЕДНЕЙ ПРИСПОСОБЛЕННОСТИ =====
        st.subheader("📈 Изменение средней приспособленности")
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(avg_fitness, marker='o', markersize=4, linewidth=1.5)
        ax4.set_xlabel('Поколение')
        ax4.set_ylabel('Средняя приспособленность')
        ax4.set_title('Динамика средней приспособленности')
        ax4.grid(True, alpha=0.3)
        st.pyplot(fig4)

        # ===== ИТОГОВЫЙ РЕЗУЛЬТАТ =====
        st.subheader("🏆 Итоговый результат")

        best_last = max(populations[generations], key=lambda ind: ind.fitness)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Лучший x", f"{best_last.x:.10f}")
        with col2:
            st.metric("Хромосома", best_last.chromosome)
        with col3:
            st.metric("f(x)", f"{best_last.f:.10f}")
        with col4:
            st.metric("F(x)", f"{best_last.fitness:.10f}")


else:  # Задание 2
    st.header("🔢 Задание №2: Поиск бинарных кодовых последовательностей")

    variant_options = list(range(1, 24))
    variant = st.selectbox("Выберите вариант (1-23)", variant_options, format_func=lambda x: f"Вариант {x}")

    generations = st.slider("Количество поколений", 50, 500, 200, key="gen2")
    seed = st.number_input("Seed (для воспроизводимости)", value=42, step=1, key="seed2")

    if st.button("🚀 Запустить ГА (поиск КП)", type="primary"):
        with st.spinner("Выполняется генетический алгоритм поиска КП..."):
            ga2 = Task2GA(variant)
            ga2.generations = generations
            populations, avg_fitness, best_psl_history, found_seqs = ga2.run(seed=seed)

        st.success("Выполнено!")

        # ===== ПАРАМЕТРЫ ВАРИАНТА =====
        st.subheader("📋 Параметры варианта")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("N (длина КП)", ga2.n)
        with col2:
            st.metric("Размер популяции (P)", ga2.population_size)
        with col3:
            st.metric("Требуемый PSL", ga2.psl_limit)
        with col4:
            st.metric("Искомое K", ga2.k)
        with col5:
            st.metric("Pk / Pm", f"{ga2.pk} / {ga2.pm}")

        col6, col7 = st.columns(2)
        with col6:
            st.metric("Формирование пар", "Случайный" if ga2.parent_select == "random" else "Лучшие с лучшими")
        with col7:
            st.metric("Селекция", "Рулетка" if ga2.selection == "roulette" else "Турнир")

        # ===== ГРАФИКИ =====
        st.subheader("📊 Динамика работы алгоритма")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # График средней приспособленности
        ax1.plot(avg_fitness, linewidth=1.5, color='blue')
        ax1.set_xlabel('Поколение')
        ax1.set_ylabel('Средняя FFn')
        ax1.set_title('Средняя приспособленность')
        ax1.grid(True, alpha=0.3)

        # График лучшего PSL
        ax2.plot(best_psl_history, linewidth=1.5, color='red')
        ax2.axhline(y=ga2.psl_limit, color='green', linestyle='--', label=f'Цель: PSL ≤ {ga2.psl_limit}')
        ax2.set_xlabel('Поколение')
        ax2.set_ylabel('Лучший PSL')
        ax2.set_title('Динамика лучшего PSL')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)

        # ===== ТАБЛИЦЫ ПОПУЛЯЦИЙ =====
        st.subheader("📋 Популяции")


        def display_kp_table(population, ga_obj, title, pop_num):
            st.markdown(f"**{title} (поколение {pop_num})**")

            data = []
            for i, ind in enumerate(population[:15], 1):
                psl = ga_obj.positive_sidelobe_level(ind.genes)
                ffn = ga_obj.fitness(ind.genes)
                data.append({
                    "№": i,
                    "КП": ind.sequence_str,
                    "PSL": psl,
                    "FFn": f"{ffn:.4f}"
                })
            st.dataframe(data, use_container_width=True)

            avg_psl = sum(ga_obj.positive_sidelobe_level(ind.genes) for ind in population) / len(population)
            avg_ffn = sum(ga_obj.fitness(ind.genes) for ind in population) / len(population)

            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"📊 Средний PSL: {avg_psl:.2f}")
            with col2:
                st.caption(f"📊 Средняя FFn: {avg_ffn:.4f}")
            st.markdown("---")


        # Выводим таблицы
        if 0 in populations:
            display_kp_table(populations[0], ga2, "НАЧАЛЬНАЯ ПОПУЛЯЦИЯ", 0)

        if 3 in populations:
            display_kp_table(populations[3], ga2, "ТРЕТЬЯ ПОПУЛЯЦИЯ", 3)

        if generations in populations:
            display_kp_table(populations[generations], ga2, "ПОСЛЕДНЯЯ ПОПУЛЯЦИЯ", generations)

        # ===== ГРАФИКИ АКФ ДЛЯ НАЙДЕННЫХ КП =====
        st.subheader("🔍 Найденные кодовые последовательности")

        if found_seqs:
            st.success(f"Найдено {len(found_seqs)} КП с PSL ≤ {ga2.psl_limit}")

            for i, seq in enumerate(found_seqs[:ga2.k]):
                psl = ga2.positive_sidelobe_level(seq.genes)
                ffn = ga2.fitness(seq.genes)

                with st.expander(f"КП #{i + 1} | PSL = {psl}, FFn = {ffn:.4f}", expanded=True):
                    st.markdown(f"**Последовательность:** `{seq.sequence_str}`")
                    st.markdown(f"**Длина N = {ga2.n}**")
                    st.markdown(f"**PSL = {psl}** (требуемый ≤ {ga2.psl_limit})")

                    # График АКФ
                    shifts, acf_vals = ga2.aperiodic_acf(seq.genes)

                    fig_acf, ax_acf = plt.subplots(figsize=(12, 5))

                    # Строим АКФ
                    ax_acf.plot(shifts, acf_vals, marker='o', markersize=4, linewidth=1.5, color='purple')
                    ax_acf.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                    ax_acf.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

                    # Выделяем боковые лепестки
                    center_idx = ga2.n - 1
                    for j, (shift, val) in enumerate(zip(shifts, acf_vals)):
                        if j != center_idx and val > 0:
                            ax_acf.plot(shift, val, 'ro', markersize=6, zorder=5)

                    ax_acf.set_xlabel('Сдвиг k')
                    ax_acf.set_ylabel('R(k)')
                    ax_acf.set_title(f'АКФ найденной КП #{i + 1} (PSL = {psl})')
                    ax_acf.grid(True, alpha=0.3)

                    st.pyplot(fig_acf)
        else:
            st.warning(f"⚠️ За {generations} поколений не найдено КП с PSL ≤ {ga2.psl_limit}")

            # Показываем лучшую найденную
            if generations in populations:
                best_ind = max(populations[generations], key=lambda ind: ga2.fitness(ind.genes))
                best_psl = ga2.positive_sidelobe_level(best_ind.genes)
                st.info(f"📌 Лучший достигнутый PSL: {best_psl} (при требуемом {ga2.psl_limit})")

                # График АКФ лучшей
                shifts, acf_vals = ga2.aperiodic_acf(best_ind.genes)
                fig_acf, ax_acf = plt.subplots(figsize=(12, 5))
                ax_acf.plot(shifts, acf_vals, marker='o', markersize=4, linewidth=1.5)
                ax_acf.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                ax_acf.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
                ax_acf.set_xlabel('Сдвиг k')
                ax_acf.set_ylabel('R(k)')
                ax_acf.set_title(f'АКФ лучшей найденной КП (PSL = {best_psl})')
                ax_acf.grid(True, alpha=0.3)
                st.pyplot(fig_acf)

            st.markdown("**Рекомендации для улучшения:**")
            st.markdown("- Увеличьте количество поколений (рекомендуется 300-500)")
            st.markdown("- Увеличьте размер популяции")
            st.markdown("- Измените seed для другого случайного поиска")
            st.markdown("- Попробуйте другой вариант")