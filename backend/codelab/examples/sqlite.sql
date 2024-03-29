
-- tabelas

create table predio (
    cod_predio smallint not null,
    nome       varchar(30) not null,

    primary key (cod_predio)
);

create index idx_predio_1 on predio(nome);


create table sala (
    cod_predio smallint not null,
    numero     smallint not null,
    capacidade numeric(5) not null,
    primary key (cod_predio, numero),

    foreign key (cod_predio) references predio
        on delete cascade
        on update cascade
);


create table depto (
    cod_depto char(3) not null,
    nome      varchar(30) not null,
    primary key (cod_depto)
);

create unique index idx_depto on depto(nome);


create table disciplina (
    cod_depto char(3) not null,
    num_disc  numeric(3) not null,
    nome      varchar(30) not null,
    creditos  numeric(2) not null,

    primary key (cod_depto, num_disc),
    foreign key (cod_depto) references depto
);


create table pre_requisito (
    cod_depto char(3) not null,
    num_disc  numeric(3) not null,
    cod_depto_pre_req char(3) not null,
    num_disc_pre_req  numeric(3) not null,

    primary key (cod_depto, num_disc, cod_depto_pre_req, num_disc_pre_req),
    foreign key (cod_depto, num_disc) references disciplina
        on delete cascade
        on update cascade,
    foreign key (cod_depto_pre_req, num_disc_pre_req) references disciplina
        on delete cascade
        on update cascade
);


create table turma (
    ano        smallint not null,
    sem        smallint not null,
    cod_depto  char(3) not null,
    num_disc   numeric(3) not null,
    sigla      char(6) not null,
    capacidade numeric(3) not null,

    primary key (ano, sem, cod_depto, num_disc, sigla),
    foreign key (cod_depto, num_disc) references disciplina
        on delete cascade
        on update cascade
);



create table horario (
    ano       smallint not null,
    sem       smallint not null,
    cod_depto char(3) not null,
    num_disc  numeric(3) not null,
    sigla     char(6) not null,
    dia_semana   numeric(1) check((1 <= dia_semana) and (dia_semana <= 7)) not null,
    hora_inicio time not null,
    num_horas   numeric(1) default 1 not null,
    cod_predio  smallint not null,
    num_sala    smallint not null,

    primary key (ano, sem, cod_depto, num_disc, sigla, dia_semana, hora_inicio),
    foreign key (ano, sem, cod_depto, num_disc, sigla) references turma
        on delete cascade
        on update cascade,
    foreign key (cod_predio, num_sala) references sala
        on delete cascade
        on update cascade
);


create table titulacao (
    cod_titulacao varchar(5) not null,
    nome          varchar(20) not null,

    primary key (cod_titulacao)
);


create table professor (
    cod_prof      smallint not null,
    nome          varchar(40) not null,
    cod_titulacao varchar(5) not null,
    cod_depto     char(3) not null,

    primary key (cod_prof),
    foreign key (cod_titulacao) references titulacao
        on delete set null
        on update set null,
    foreign key (cod_depto) references depto
);

create index idx_professor_1 on professor (nome);


create table prof_turma (
    ano        smallint not null,
    sem        smallint not null,
    cod_depto  char(3) not null,
    num_disc   numeric(3) not null,
    sigla      char(6) not null,
    cod_prof   smallint not null,

    primary key (ano, sem, cod_depto, num_disc, cod_prof),
    foreign key (ano, sem, cod_depto, num_disc, sigla) references turma
        on delete cascade
        on update cascade,

    foreign key (cod_prof) references professor
        on delete set null
        on update cascade
);

-- Dados

insert into predio values (1, 'Hilton');
insert into predio values (2, 'Plazza');
insert into predio values (3, 'Alfa');
insert into predio values (4, 'Teta');
insert into predio values (5, 'Gama');
insert into predio values (6, 'Bloco A');
insert into predio values (7, 'Bloco B');
insert into predio values (8, 'Bloco C');
insert into predio values (9, 'Bloco D');
insert into predio values (10, 'Bloco E');
insert into predio values (3421, 'Prédio de Malucos');
insert into predio values (3422, 'Argentina');
insert into predio values (3423, 'Europa');
insert into predio values (3424, 'Italia');
insert into predio values (3425, 'japao');
insert into predio values (3426, 'Alemanha');
insert into predio values (3427, 'Chile');

insert into sala values (1, 1, 40);
insert into sala values (1, 10, 53);
insert into sala values (1, 11, 52);
insert into sala values (1, 12, 94);
insert into sala values (1, 13, 56);
insert into sala values (1, 14, 90);
insert into sala values (1, 15, 30);
insert into sala values (1, 16, 40);
insert into sala values (1, 17, 50);
insert into sala values (1, 18, 80);
insert into sala values (1, 19, 25);
insert into sala values (1, 2, 40);
insert into sala values (1, 20, 49);
insert into sala values (1, 3, 30);
insert into sala values (1, 4, 40);
insert into sala values (1, 5, 25);
insert into sala values (1, 6, 98);
insert into sala values (1, 7, 54);
insert into sala values (1, 8, 68);
insert into sala values (1, 9, 48);
insert into sala values (10, 1, 77);
insert into sala values (10, 10, 24);
insert into sala values (10, 11, 66);
insert into sala values (10, 12, 33);
insert into sala values (10, 13, 53);
insert into sala values (10, 14, 42);
insert into sala values (10, 15, 64);
insert into sala values (10, 16, 85);
insert into sala values (10, 17, 71);
insert into sala values (10, 18, 58);
insert into sala values (10, 19, 59);
insert into sala values (10, 2, 29);
insert into sala values (10, 20, 73);
insert into sala values (10, 3, 30);
insert into sala values (10, 4, 63);
insert into sala values (10, 5, 32);
insert into sala values (10, 6, 44);
insert into sala values (10, 7, 20);
insert into sala values (10, 8, 76);
insert into sala values (10, 9, 68);
insert into sala values (2, 1, 45);
insert into sala values (2, 2, 40);
insert into sala values (2, 3, 80);
insert into sala values (2, 4, 40);
insert into sala values (2, 5, 25);
insert into sala values (3, 1, 40);
insert into sala values (3, 10, 44);
insert into sala values (3, 11, 72);
insert into sala values (3, 12, 28);
insert into sala values (3, 13, 80);
insert into sala values (3, 14, 78);
insert into sala values (3, 15, 28);
insert into sala values (3, 16, 32);
insert into sala values (3, 17, 37);
insert into sala values (3, 18, 78);
insert into sala values (3, 19, 26);
insert into sala values (3, 2, 40);
insert into sala values (3, 20, 76);
insert into sala values (3, 3, 30);
insert into sala values (3, 4, 40);
insert into sala values (3, 5, 25);
insert into sala values (3, 6, 84);
insert into sala values (3, 7, 34);
insert into sala values (3, 8, 82);
insert into sala values (3, 9, 46);
insert into sala values (4, 1, 58);
insert into sala values (4, 10, 61);
insert into sala values (4, 11, 92);
insert into sala values (4, 12, 69);
insert into sala values (4, 13, 81);
insert into sala values (4, 14, 34);
insert into sala values (4, 15, 63);
insert into sala values (4, 16, 69);
insert into sala values (4, 17, 36);
insert into sala values (4, 18, 77);
insert into sala values (4, 19, 66);
insert into sala values (4, 2, 67);
insert into sala values (4, 20, 73);
insert into sala values (4, 3, 76);
insert into sala values (4, 4, 92);
insert into sala values (4, 5, 26);
insert into sala values (4, 6, 100);
insert into sala values (4, 7, 41);
insert into sala values (4, 8, 46);
insert into sala values (4, 9, 51);
insert into sala values (3421, 1, 25);
insert into sala values (3421, 10, 50);
insert into sala values (3421, 101, 50);
insert into sala values (3421, 11, 50);
insert into sala values (3421, 12, 100);
insert into sala values (3421, 13, 50);
insert into sala values (3421, 14, 60);
insert into sala values (3421, 15, 30);
insert into sala values (3421, 16, 90);
insert into sala values (3421, 17, 80);
insert into sala values (3421, 18, 50);
insert into sala values (3421, 19, 79);
insert into sala values (3421, 2, 25);
insert into sala values (3421, 201, 150);
insert into sala values (3421, 203, 20);
insert into sala values (3421, 207, 70);
insert into sala values (3421, 3, 48);
insert into sala values (3421, 301, 150);
insert into sala values (3421, 302, 40);
insert into sala values (3421, 4, 33);
insert into sala values (3421, 401, 50);
insert into sala values (3421, 5, 90);
insert into sala values (3421, 6, 90);
insert into sala values (3421, 7, 40);
insert into sala values (3421, 8, 60);
insert into sala values (3421, 9, 40);
insert into sala values (3422, 101, 50);
insert into sala values (3422, 201, 150);
insert into sala values (3422, 203, 20);
insert into sala values (3422, 207, 70);
insert into sala values (3422, 301, 150);
insert into sala values (3422, 302, 40);
insert into sala values (3422, 401, 50);
insert into sala values (3423, 101, 50);
insert into sala values (3423, 201, 150);
insert into sala values (3423, 203, 200);
insert into sala values (3423, 207, 70);
insert into sala values (3423, 301, 1500);
insert into sala values (3423, 302, 400);
insert into sala values (3423, 401, 150);
insert into sala values (3424, 101, 150);
insert into sala values (3424, 201, 1150);
insert into sala values (3424, 203, 200);
insert into sala values (3424, 207, 170);
insert into sala values (3425, 301, 150);
insert into sala values (3425, 302, 40);
insert into sala values (3425, 401, 50);
insert into sala values (3426, 101, 50);
insert into sala values (3426, 201, 150);
insert into sala values (3426, 203, 20);
insert into sala values (3427, 207, 70);
insert into sala values (3427, 301, 150);
insert into sala values (3427, 302, 40);
Insert into sala values (3427, 401, 50);
insert into sala values (5, 1, 20);
insert into sala values (5, 10, 72);
insert into sala values (5, 11, 63);
insert into sala values (5, 12, 57);
insert into sala values (5, 13, 67);
insert into sala values (5, 14, 51);
insert into sala values (5, 15, 64);
insert into sala values (5, 16, 50);
insert into sala values (5, 17, 51);
insert into sala values (5, 18, 32);
insert into sala values (5, 19, 75);
insert into sala values (5, 2, 74);
insert into sala values (5, 20, 44);
insert into sala values (5, 3, 77);
insert into sala values (5, 4, 80);
insert into sala values (5, 5, 85);
insert into sala values (5, 6, 72);
insert into sala values (5, 7, 83);
insert into sala values (5, 8, 76);
insert into sala values (5, 9, 60);
insert into sala values (6, 1, 54);
insert into sala values (6, 10, 82);
insert into sala values (6, 11, 57);
insert into sala values (6, 12, 42);
insert into sala values (6, 13, 33);
insert into sala values (6, 14, 57);
insert into sala values (6, 15, 46);
insert into sala values (6, 16, 67);
insert into sala values (6, 17, 74);
insert into sala values (6, 18, 52);
insert into sala values (6, 19, 68);
insert into sala values (6, 2, 30);
insert into sala values (6, 20, 48);
insert into sala values (6, 3, 61);
insert into sala values (6, 4, 78);
insert into sala values (6, 5, 48);
insert into sala values (6, 6, 62);
insert into sala values (6, 7, 51);
insert into sala values (6, 8, 46);
insert into sala values (6, 9, 91);
insert into sala values (7, 1, 39);
insert into sala values (7, 10, 66);
insert into sala values (7, 11, 36);
insert into sala values (7, 12, 30);
insert into sala values (7, 13, 32);
insert into sala values (7, 14, 43);
insert into sala values (7, 15, 100);
insert into sala values (7, 16, 62);
insert into sala values (7, 17, 38);
insert into sala values (7, 18, 58);
insert into sala values (7, 19, 55);
insert into sala values (7, 2, 51);
insert into sala values (7, 20, 57);
insert into sala values (7, 3, 37);
insert into sala values (7, 4, 24);
insert into sala values (7, 5, 79);
insert into sala values (7, 6, 64);
insert into sala values (7, 7, 89);
insert into sala values (7, 8, 82);
insert into sala values (7, 9, 49);
insert into sala values (8, 1, 58);
insert into sala values (8, 10, 28);
insert into sala values (8, 11, 81);
insert into sala values (8, 12, 77);
insert into sala values (8, 13, 45);
insert into sala values (8, 14, 20);
insert into sala values (8, 15, 44);
insert into sala values (8, 16, 53);
insert into sala values (8, 17, 22);
insert into sala values (8, 18, 96);
insert into sala values (8, 19, 36);
insert into sala values (8, 2, 62);
insert into sala values (8, 20, 35);
insert into sala values (8, 3, 56);
insert into sala values (8, 4, 41);
insert into sala values (8, 5, 69);
insert into sala values (8, 6, 41);
insert into sala values (8, 7, 73);
insert into sala values (8, 8, 99);
insert into sala values (8, 9, 48);
insert into sala values (9, 1, 96);
insert into sala values (9, 10, 21);
insert into sala values (9, 11, 24);
insert into sala values (9, 12, 57);
insert into sala values (9, 13, 21);
insert into sala values (9, 14, 97);
insert into sala values (9, 15, 27);
insert into sala values (9, 16, 59);
insert into sala values (9, 17, 46);
insert into sala values (9, 18, 53);
insert into sala values (9, 19, 40);
insert into sala values (9, 2, 94);
insert into sala values (9, 20, 70);
insert into sala values (9, 3, 31);
insert into sala values (9, 4, 32);
insert into sala values (9, 5, 38);
insert into sala values (9, 6, 58);
insert into sala values (9, 7, 79);
insert into sala values (9, 8, 78);
insert into sala values (9, 9, 49);





insert into depto values ('ADM', 'Administração');
insert into depto values ('ARQ', 'Arquitetura');
insert into depto values ('CMX', 'Comercio Exterior');
insert into depto values ('DIR', 'Direito');
insert into depto values ('EDU', 'Educacao Fisica');
insert into depto values ('ENF', 'Enfermagem');
insert into depto values ('ENG', 'Engenharia');
insert into depto values ('FAR', 'Farmacia');
insert into depto values ('FIS', 'Fisioterapia');
insert into depto values ('INF', 'Informática');
insert into depto values ('MED', 'Medicina');
insert into depto values ('TUR', 'Turismo');
insert into depto values ('VET', 'Veterinária');





insert into disciplina values ('ADM', 320, 'Administracao I', 1);
insert into disciplina values ('ADM', 321, 'Analise Estruturada', 4);
insert into disciplina values ('ADM', 01, 'CON I', 7);
insert into disciplina values ('ADM', 02, 'CON II', 4);
insert into disciplina values ('ARQ', 1, 'URB1', 6);
insert into disciplina values ('ARQ', 2, 'CALC1', 5);
insert into disciplina values ('CMX', 420, 'Com Exterior I', 2);
insert into disciplina values ('CMX', 421, 'Com Exterior II', 3);
insert into disciplina values ('CMX', 422, 'Com Exterior III', 4);
insert into disciplina values ('CMX', 423, 'Com Exterior IV', 2);
insert into disciplina values ('CMX', 1, 'Economia', 5);
insert into disciplina values ('CMX', 2, 'Administração', 6);
insert into disciplina values ('CMX', 3, 'Comex', 10);
insert into disciplina values ('CMX', 4, 'Imortação', 6);
insert into disciplina values ('CMX', 5, 'Psicologia', 8);
insert into disciplina values ('DIR', 220, 'Codigo Civil', 7);
insert into disciplina values ('DIR', 221, 'Leis do Trabalho', 4);
insert into disciplina values ('DIR', 222, 'Direito ', 3);
insert into disciplina values ('DIR', 223, 'Legislacao', 12);
insert into disciplina values ('DIR', 322, 'Adminsitracao II', 5);
insert into disciplina values ('ENG', 1, 'MEC I', 6);
insert into disciplina values ('ENG', 2, 'MEC II', 3);
insert into disciplina values ('INF', 1, 'SBD I', 5);
insert into disciplina values ('INF', 10, 'Lógica Matemática', 3);
insert into disciplina values ('INF', 11, 'Computação Gráfica', 4);
insert into disciplina values ('INF', 12, 'C++', 4);
insert into disciplina values ('INF', 120, 'Log Programacao I', 7);
insert into disciplina values ('INF', 121, 'Log Programacao II', 4);
insert into disciplina values ('INF', 122, 'Log Programacao III ', 3);
insert into disciplina values ('INF', 123, 'Log digital I', 12);
insert into disciplina values ('INF', 124, 'Logica Matematica', 3);
insert into disciplina values ('INF', 125, 'Calculo I', 2);
insert into disciplina values ('INF', 13, 'Turbo Pascal', 8);
insert into disciplina values ('INF', 2, 'SBD II', 6);
insert into disciplina values ('INF', 3, 'TLP3', 6);
insert into disciplina values ('INF', 4, 'LP3', 7);
insert into disciplina values ('INF', 5, 'LP6', 5);
insert into disciplina values ('INF', 6, 'Ling Formais e Compiladores', 9);
insert into disciplina values ('INF', 7, 'Arquitetura de Computadores', 4);
insert into disciplina values ('INF', 8, 'Geometria Analítica', 2);
insert into disciplina values ('INF', 9, 'Matemática Financeira', 10);




insert into pre_requisito values ('INF', 7, 'INF', 6);
insert into pre_requisito values ('INF', 7, 'INF', 5);
insert into pre_requisito values ('INF', 8, 'INF', 6);
insert into pre_requisito values ('INF', 3, 'INF', 2);
insert into pre_requisito values ('INF', 5, 'INF', 3);
insert into pre_requisito values ('INF', 5, 'INF', 4);
insert into pre_requisito values ('ENG', 2, 'ENG', 1);
insert into pre_requisito values ('ADM', 2, 'ADM', 1);
insert into pre_requisito values ('INF', 12, 'INF', 2);
insert into pre_requisito values ('INF', 13, 'INF', 2);
insert into pre_requisito values ('INF', 10, 'INF', 5);
insert into pre_requisito values ('ADM', 321, 'ADM', 320);
insert into pre_requisito values ('CMX', 422, 'CMX', 421);
insert into pre_requisito values ('CMX', 421 , 'CMX', 420);
insert into pre_requisito values ('INF', 122 , 'INF', 121);
insert into pre_requisito values ('INF', 122 , 'INF', 120);
insert into pre_requisito values ('INF', 121 , 'INF', 120);



insert into turma values (1999, 1, 'INF', 1,    'Q',     60);
insert into turma values (1999, 1, 'INF', 3,    'R',     80);
insert into turma values (1999, 1, 'INF', 5,    'R',     80);
insert into turma values (2000, 1, 'ADM', 320,  'ADM',   30);
insert into turma values (2000, 1, 'DIR', 220,  'DIR1',  15);
insert into turma values (2000, 1, 'INF', 1,    'P',     80);
insert into turma values (2000, 1, 'INF', 1,    'Q',     100);
insert into turma values (2000, 1, 'INF', 120,  'INFBAS', 15);
insert into turma values (2000, 2, 'ADM', 321,  'ADM',    30);
insert into turma values (2000, 2, 'INF', 1,    'P',      70);
insert into turma values (2000, 2, 'INF', 1,    'Q',      60);
insert into turma values (2001, 1, 'CMX', 420,  'CMX1',   40);
insert into turma values (2001, 1, 'CMX', 421,  'CMX21',  40);
insert into turma values (2001, 1, 'INF', 1,    'SBD1',   40);
insert into turma values (2001, 1, 'INF', 121,  'INF2',   35);
insert into turma values (2001, 1, 'INF', 2,    'Q',      40);
insert into turma values (2001, 1, 'INF', 4,    'LP3',    25);
insert into turma values (2001, 2, 'ARQ', 1,    'URB1',   60);
insert into turma values (2001, 2, 'DIR', 221,  'DIR1',   30);
insert into turma values (2001, 2, 'INF', 1,    'SBD1',   40);
insert into turma values (2001, 2, 'INF', 2,    'Q',      40);
insert into turma values (2001, 3, 'DIR', 223,  'DIR2',   25);
insert into turma values (2002, 1, 'ADM', 320,  'ADM2',   30);
insert into turma values (2002, 1, 'ADM', 1,    'A1P05',  70);
insert into turma values (2002, 1, 'ARQ', 1,    'URB1',   60);
insert into turma values (2002, 1, 'ARQ', 2,    'CALC1',  50);
insert into turma values (2002, 1, 'CMX', 421,  'CMX2',   35);
insert into turma values (2002, 1, 'CMX', 1,    'w',      80);
insert into turma values (2002, 1, 'CMX', 2,    'w',      80);
insert into turma values (2002, 1, 'CMX', 3,    'w',      80);
insert into turma values (2002, 1, 'CMX', 4,    'w',      80);
insert into turma values (2002, 1, 'DIR', 220,  'DIR2',   20);
insert into turma values (2002, 1, 'ENG', 01,   'E1P01',  70);
insert into turma values (2002, 1, 'INF', 1,    't',      50);
insert into turma values (2002, 1, 'INF', 1,    'X',      80);
insert into turma values (2002, 1, 'INF', 120,  'INF2',   15);
insert into turma values (2002, 1, 'INF', 122,  'INFBAS', 15);
insert into turma values (2002, 1, 'INF', 2,    'SBD2',   60);
insert into turma values (2002, 1, 'INF', 2,    'X',      80);
insert into turma values (2002, 1, 'INF', 3,    'Q',      50);
insert into turma values (2002, 1, 'INF', 3,    'TLP3',   60);
insert into turma values (2002, 1, 'INF', 3,    'X',      80);
insert into turma values (2002, 1, 'INF', 4,    'LP3',    70);
insert into turma values (2002, 1, 'INF', 4,    'Q',      50);
insert into turma values (2002, 1, 'INF', 4,    'X',      80);
insert into turma values (2002, 1, 'INF', 5,    'LP6',    50);
insert into turma values (2002, 1, 'INF', 6,    'Q',      50);
insert into turma values (2002, 1, 'INF', 7,    'w',      80);
insert into turma values (2002, 1, 'INF', 8,    'w',      80);
insert into turma values (2002, 2, 'CMX', 422,  'CMX2',   40);
insert into turma values (2002, 2, 'ENG', 2,    'E2P01',  70);
insert into turma values (2002, 2, 'INF', 2,    'C2P12',  70);
insert into turma values (2002, 2, 'INF', 2,    'SBD2',   60);
insert into turma values (2002, 2, 'INF', 3,    'C2P12',  70);
insert into turma values (2002, 2, 'INF', 3,    'Q',      60);
insert into turma values (2002, 2, 'INF', 3,    'TLP3',   60);
insert into turma values (2002, 2, 'INF', 4,    'Q',      60);
insert into turma values (2002, 2, 'INF', 5,    'LP6',    50);
insert into turma values (2002, 2, 'INF', 6,    'C2P12',  70);
insert into turma values (2002, 2, 'INF', 6,    'Q',      60);
insert into turma values (2003, 1, 'INF', 1,    'C1P10',  60);
insert into turma values (2003, 1, 'INF', 2,    'C1P10',  50);
insert into turma values (2003, 1, 'INF', 3,    'C1P10',  50);
insert into turma values (2003, 1, 'INF', 4,    'C5P10',  50);
insert into turma values (2003, 1, 'INF', 5,    'C1P12',  70);
insert into turma values (2003, 1, 'INF', 6,    'C1P10',  50);
insert into turma values (2003, 1, 'INF', 7,    'C1P12',  50);
insert into turma values (2003, 1, 'INF', 8,    'C1P12',  40);
insert into turma values (2003, 1, 'INF', 9,    'C1P12',  100);
insert into turma values (2003, 2, 'ADM', 2,    'A2P05',  70);
insert into turma values (2003, 2, 'ARQ', 2,    'CALC1',  50);



insert into horario values (1999, 1, 'INF', 1, 'Q', 2, '9:00', 2, 4, 8);
insert into horario values (1999, 1, 'INF', 3, 'R', 3, '9:00', 2, 4, 9);
insert into horario values (1999, 1, 'INF', 5, 'R', 2, '9:00', 2, 5, 1);
insert into horario values (2000, 1, 'INF', 1, 'P', 2, '8:30', 2, 1, 2);
insert into horario values (2000, 1, 'INF', 1, 'Q', 3, '7:45', 2, 2, 1);
insert into horario values (2000, 2, 'INF', 1, 'P', 2, '8:30', 2, 2, 1);
insert into horario values (2000, 2, 'INF', 1, 'Q', 2, '8:30', 2, 3, 4);
insert into horario values (2001, 1, 'INF', 2, 'Q', 4, '8:30', 2, 3, 5);
insert into horario values (2001, 2, 'INF', 2, 'Q', 4, '8:35', 2, 1, 1);
insert into horario values (2002, 1, 'CMX', 1, 'w', 2, '9:00', 2, 6, 2);
insert into horario values (2002, 1, 'CMX', 2, 'w', 2, '8:30', 2, 6, 3);
insert into horario values (2002, 1, 'CMX', 3, 'w', 5, '9:00', 2, 6, 4);
insert into horario values (2002, 1, 'CMX', 4, 'w', 3, '8:30', 2, 6, 5);
insert into horario values (2002, 1, 'INF', 1, 't', 2, '8:30', 2, 6, 5);
insert into horario values (2002, 1, 'INF', 1, 'X', 2, '8:30', 2, 5, 2);
insert into horario values (2002, 1, 'INF', 2, 'X', 5, '8:30', 2, 5, 3);
insert into horario values (2002, 1, 'INF', 2, 'X', 3, '8:30', 2, 5, 3);

insert into horario values (2002, 1, 'INF', 3, 'Q', 1, '8:30', 2, 5, 3);
insert into horario values (2002, 1, 'INF', 3, 'X', 4, '9:00', 2, 5, 4);
insert into horario values (2002, 1, 'INF', 4, 'Q', 7, '8:30', 2, 1, 1);
insert into horario values (2002, 1, 'INF', 4, 'X', 5, '9:00', 2, 5, 5);
insert into horario values (2002, 1, 'INF', 6, 'Q', 5, '9:00', 2, 4, 4);
insert into horario values (2002, 1, 'INF', 6, 'Q', 2, '9:00', 2, 5, 7);
insert into horario values (2002, 1, 'INF', 7, 'w', 4, '9:00', 2, 7, 1);
insert into horario values (2002, 1, 'INF', 8, 'w', 5, '9:00', 2, 6, 1);
insert into horario values (2002, 2, 'INF', 3, 'Q', 2, '9:00', 2, 4, 1);
insert into horario values (2002, 2, 'INF', 4, 'Q', 4, '9:00', 2, 4, 3);
insert into horario values (2002, 2, 'INF', 6, 'Q', 3, '9:00', 2, 4, 2);
insert into horario values (2003, 1, 'INF', 8, 'C1P12', 4, '9:00', 2, 4, 5);
insert into horario values (2003, 1, 'INF', 8, 'C1P12', 5, '9:00', 2, 4, 7);
insert into horario values (2002, 2, 'CMX', 422, 'CMX2', 2, '8:30', 2, 6, 3);
insert into horario values (2002, 2, 'ENG', 2, 'E2P01', 5, '9:00', 2, 6, 4);
insert into horario values (2002, 2, 'INF', 2, 'C2P12', 3, '8:30', 2, 6, 5);
insert into horario values (2002, 2, 'INF', 2, 'SBD2',  2, '8:30', 2, 6, 5);
insert into horario values (2002, 2, 'INF', 2, 'SBD2',  4, '8:30', 2, 6, 5);
insert into horario values (2002, 2, 'INF', 3, 'C2P12', 2, '8:30', 2, 5, 2);
insert into horario values (2002, 2, 'INF', 3, 'Q',     5, '8:30', 2, 5, 3);
insert into horario values (2002, 2, 'INF', 3, 'TLP3',  1, '8:30', 2, 5, 3);
insert into horario values (2002, 2, 'INF', 4, 'Q',     3, '9:00', 2, 5, 4);
insert into horario values (2002, 2, 'INF', 5, 'LP6',   7, '8:30', 2, 1, 1);
insert into horario values (2002, 2, 'INF', 6, 'C2P12', 5, '9:00', 2, 5, 5);
insert into horario values (2002, 2, 'INF', 6, 'C2P12', 3, '9:00', 2, 5, 6);
insert into horario values (2003, 1, 'INF', 1, 'C1P10', 5, '9:00', 2, 4, 4);
insert into horario values (2003, 1, 'INF', 2, 'C1P10', 2, '9:00', 2, 5, 7);
insert into horario values (2003, 1, 'INF', 3, 'C1P10', 4, '9:00', 2, 7, 1);
insert into horario values (2003, 1, 'INF', 4, 'C5P10', 5, '9:00', 2, 6, 1);
insert into horario values (2003, 1, 'INF', 5, 'C1P12', 2, '9:00', 2, 4, 1);
insert into horario values (2003, 1, 'INF', 6, 'C1P10', 4, '9:00', 2, 4, 3);
insert into horario values (2003, 1, 'INF', 7, 'C1P12', 3, '9:00', 2, 4, 2);
insert into horario values (2003, 1, 'INF', 8, 'C1P12', 2, '9:00', 2, 4, 5);
insert into horario values (2003, 1, 'INF', 9, 'C1P12', 4, '9:00', 2, 4, 7);



insert into titulacao values ('Dr.', 'Doutorado');
insert into titulacao values ('MSc.', 'Mestrado');
insert into titulacao values ('Esp.', 'Especialização');


insert into professor values (11,  'Andre',  'Dr.', 'INF');
insert into professor values (12,  'Daniel', 'Dr.', 'INF');
insert into professor values (13,  'Cintia', 'Dr.', 'INF');
insert into professor values (14,  'Raul',   'Dr.', 'INF');
insert into professor values (15,  'Rafael', 'MSc.', 'INF');
insert into professor values (16,  'Joao',   'Dr.', 'ENG');
insert into professor values (17,  'Jose',   'Esp.', 'ADM');
insert into professor values (1,   'Galessandro', 'Dr.',  'INF');
insert into professor values (2,   'Tizzei',      'Dr.',  'INF');
insert into professor values (3,   'Rosani',      'Dr.',  'INF');
insert into professor values (4,   'João Bosco',  'Dr.',  'INF');
insert into professor values (5,   'Fernando',    'MSc.', 'INF');
insert into professor values (6,   'Mariana',     'Dr.',  'INF');
insert into professor values (7,   'Guilherme',   'Esp.', 'ENG');
insert into professor values (101, 'Valdomiro Filho', 'MSc.', 'INF');
insert into professor values (102, 'Adamastor Nepomuceno', 'Dr.', 'INF');
insert into professor values (103, 'Jose da Silva', 'MSc.', 'INF');
insert into professor values (104, 'Marlete de Lurdes', 'Dr.', 'ADM');
insert into professor values (105, 'Virgulino Salgado', 'Dr.', 'CMX');
insert into professor values (106, 'Francisco Anisio', 'Dr.', 'MED');
insert into professor values (107, 'Carla Perez', 'Dr.', 'EDU');
insert into professor values (109, 'Tom Cavalcante', 'MSc.', 'DIR');
insert into professor values (110, 'Pedro Alvares Cabral', 'MSc.', 'TUR');
insert into professor values (111, 'Rubens Barrichelo', 'Dr.', 'INF');



insert into prof_turma values (1999, 1, 'INF', 1,    'Q',     11);
insert into prof_turma values (1999, 1, 'INF', 3,    'R',     12);
insert into prof_turma values (1999, 1, 'INF', 5,    'R',     13);
insert into prof_turma values (2000, 1, 'ADM', 320,  'ADM',   14);
insert into prof_turma values (2000, 1, 'DIR', 220,  'DIR1',  15);
insert into prof_turma values (2000, 1, 'INF', 1,    'P',     16);
insert into prof_turma values (2000, 1, 'INF', 1,    'Q',     17);
insert into prof_turma values (2000, 1, 'INF', 120,  'INFBAS', 1);
insert into prof_turma values (2000, 2, 'ADM', 321,  'ADM',   2);
insert into prof_turma values (2000, 2, 'INF', 1,    'P',     3);
insert into prof_turma values (2000, 2, 'INF', 1,    'Q',     4);
insert into prof_turma values (2001, 1, 'CMX', 420,  'CMX1',  5);
insert into prof_turma values (2001, 1, 'CMX', 421,  'CMX21', 6);
insert into prof_turma values (2001, 1, 'INF', 1,    'SBD1',  7);
insert into prof_turma values (2001, 1, 'INF', 121,  'INF2',  101);
insert into prof_turma values (2001, 1, 'INF', 2,    'Q',     102);
insert into prof_turma values (2001, 1, 'INF', 4,    'LP3',   103);
insert into prof_turma values (2001, 2, 'ARQ', 1,    'URB1',  104);
insert into prof_turma values (2001, 2, 'DIR', 221,  'DIR1',  105);
insert into prof_turma values (2001, 2, 'INF', 1,    'SBD1',  106);
insert into prof_turma values (2001, 2, 'INF', 2,    'Q',     107);
insert into prof_turma values (2001, 3, 'DIR', 223,  'DIR2',  109);
insert into prof_turma values (2002, 1, 'ADM', 1,    'A1P05', 111);
insert into prof_turma values (2002, 1, 'ADM', 320,  'ADM2',  110);
insert into prof_turma values (2002, 1, 'ARQ', 1,    'URB1',  101);
insert into prof_turma values (2002, 1, 'ARQ', 2,    'CALC1', 102);
insert into prof_turma values (2002, 1, 'CMX', 1,    'w',     104);
insert into prof_turma values (2002, 1, 'CMX', 2,    'w',     105);
insert into prof_turma values (2002, 1, 'CMX', 3,    'w',     106);
insert into prof_turma values (2002, 1, 'CMX', 4,    'w',     107);
insert into prof_turma values (2002, 1, 'CMX', 421,  'CMX2',  103);
insert into prof_turma values (2002, 1, 'DIR', 220,  'DIR2',  109);
insert into prof_turma values (2002, 1, 'ENG', 01,   'E1P01', 110);
insert into prof_turma values (2002, 1, 'INF', 1,    't',     111);
insert into prof_turma values (2002, 1, 'INF', 1,    'X',     101);
insert into prof_turma values (2002, 1, 'INF', 120,  'INF2',  102);
insert into prof_turma values (2002, 1, 'INF', 122,  'INFBAS', 103);
insert into prof_turma values (2002, 1, 'INF', 2,    'SBD2',  104);
insert into prof_turma values (2002, 1, 'INF', 2,    'X',     105);
insert into prof_turma values (2002, 1, 'INF', 3,    'Q',     106);
insert into prof_turma values (2002, 1, 'INF', 3,    'TLP3',  107);
insert into prof_turma values (2002, 1, 'INF', 3,    'X',     109);
insert into prof_turma values (2002, 1, 'INF', 4,    'LP3',   110);
insert into prof_turma values (2002, 1, 'INF', 4,    'Q',     111);
insert into prof_turma values (2002, 1, 'INF', 4,    'X',     101);
insert into prof_turma values (2002, 1, 'INF', 5,    'LP6',   102);
insert into prof_turma values (2002, 1, 'INF', 6,    'Q',     103);
insert into prof_turma values (2002, 1, 'INF', 7,    'w',     104);
insert into prof_turma values (2002, 1, 'INF', 8,    'w',     105);
insert into prof_turma values (2002, 2, 'CMX', 422,  'CMX2',  106);
insert into prof_turma values (2002, 2, 'ENG', 2,    'E2P01', 107);
insert into prof_turma values (2002, 2, 'INF', 2,    'C2P12', 109);
insert into prof_turma values (2002, 2, 'INF', 2,    'SBD2',  110);
insert into prof_turma values (2002, 2, 'INF', 3,    'C2P12', 111);
insert into prof_turma values (2002, 2, 'INF', 3,    'Q',     101);
insert into prof_turma values (2002, 2, 'INF', 3,    'TLP3',  102);
insert into prof_turma values (2002, 2, 'INF', 4,    'Q',     103);
insert into prof_turma values (2002, 2, 'INF', 5,    'LP6',   104);
insert into prof_turma values (2002, 2, 'INF', 6,    'C2P12', 105);
insert into prof_turma values (2002, 2, 'INF', 6,    'Q',     106);
insert into prof_turma values (2003, 1, 'INF', 1,    'C1P10', 107);
insert into prof_turma values (2003, 1, 'INF', 2,    'C1P10', 109);
insert into prof_turma values (2003, 1, 'INF', 3,    'C1P10', 110);
insert into prof_turma values (2003, 1, 'INF', 4,    'C5P10', 111);
insert into prof_turma values (2003, 1, 'INF', 5,    'C1P12', 101);
insert into prof_turma values (2003, 1, 'INF', 6,    'C1P10', 102);
insert into prof_turma values (2003, 1, 'INF', 7,    'C1P12', 103);
insert into prof_turma values (2003, 1, 'INF', 8,    'C1P12', 104);


-- Consultas

.echo on

-- a) Obter os nomes de todas as disciplinas com mais de cinco créditos

select
    nome
from
    disciplina d
where
    d.creditos > 5;


-- b) Obter o ano/semestre em que todas as disciplinas
--    do departamento de código ‘INF’ foram oferecidas

select distinct
    ano,
    sem
from
    turma t
where
    t.cod_depto = 'INF';


-- c) Obter o nome de todas as disciplinas do departamento denominado ‘Informática’

select
    d.nome
from
    disciplina d,
    depto
where
    d.cod_depto = depto.cod_depto and
    depto.nome = 'Informática';


-- d) Obter o nome de todas as disciplinas ministradas no ano/semestre 2002/1
--    por professores vinculados ao departamento denominado ‘Informática’

select
    d.nome
from
    disciplina d
inner join
    prof_turma pf
on
    d.cod_depto = pf.cod_depto and
    d.num_disc = pf.num_disc and
    pf.ano = 2002 and
    pf.sem = 1
inner join
    depto
on
    depto.nome = 'Informática' and
    depto.cod_depto = pf.cod_depto;


-- e) Obter o nome de todos os professores que ministram alguma disciplina
--    que não seja do departamento ao qual está vinculado;

select
    nome
from
    prof_turma pf,
    professor p
where
    pf.cod_prof = p.cod_prof and
    pf.cod_depto <> p.cod_depto;


-- f) Obter a quantidade de salas do prédio de código 3421;

select
    count(*)
from
    sala
where
    cod_predio = 3421;


-- g) Obter os nomes dos professores que possuem título denominado ‘Dr.’
--    e que ministraram em 2002/1 mais que duas turmas;

select
   professor.nome,
   count(professor.cod_prof)
from
    prof_turma,
    professor,
    titulacao
where
    prof_turma.ano = 2002 and
    prof_turma.sem = 1 and
    prof_turma.cod_prof = professor.cod_prof and
    titulacao.nome = 'Doutorado' and
    titulacao.cod_titulacao = professor.cod_titulacao
group by
    professor.nome
having
    count(professor.cod_prof) > 2;


-- h) Para cada prédio que possui mais que 5 salas, obter o código do prédio,
--    seu nome e sua capacidade total;

select
    nome,
    sum(capacidade)
from
    sala,
    predio
where
    sala.cod_predio = predio.cod_predio
group by
    predio.cod_predio,
    nome
having
    count(sala.cod_predio) > 5;


-- i) Para cada professor, obter seu código, seu nome e o total de créditos por ele ministrados

select
    professor.cod_prof,
    professor.nome,
    sum(creditos)
from
    professor,
    prof_turma,
    disciplina
where
    professor.cod_prof = prof_turma.cod_prof and
    prof_turma.cod_depto = disciplina.cod_depto and
    prof_turma.num_disc = disciplina.num_disc
group by
    professor.cod_prof,
    professor.nome
order by
    professor.nome;


-- j) Crie uma visão para uma tabela contendo a identificação e o nome
--    de todas as disciplinas de mais de três créditos;

create view disc_mais_q_3cr as
    select
        cod_depto,
        num_disc
    from
        disciplina d
    where
        d.creditos > 3;


-- k) Exclua todas as linhas de disciplinas do departamento denominado ‘Fisioterapia’;

delete from
    disciplina
where
    cod_depto = (
        select
            cod_depto
        from
            depto
        where
            nome = 'Fisioterapia'
    );


-- l) Aumente em 10% a capacidade de todas as turmas de 2003/1 e 2003/2
--    das disciplinas do departamento de ‘Informática’;

update
    turma
set
    capacidade = capacidade * 1.1
where
    ano = 2003 and
    sem between 1 and 2 and
    cod_depto = (
        select
            cod_depto
        from
            depto
        where
            nome = 'Informática'
    );


-- m) Obter os nomes das disciplinas que possuem o maior número de créditos

select
    *
from
    disciplina
where
    creditos = (
        select
            max(creditos)
        from
            disciplina
    );


-- n) Apenas para cada disciplina que possua pré-requisito,
--    obter o seu nome e o nome de cada um dos seus pré-requisitos

select
    disc.nome,
    disc_pr.nome as nome_pr
from
    disciplina disc,
    disciplina disc_pr,
    pre_requisito pre_req
where
    disc.cod_depto            = pre_req.cod_depto and
    disc.num_disc             = pre_req.num_disc and
    pre_req.cod_depto_pre_req = disc_pr.cod_depto and
    pre_req.num_disc_pre_req  = disc_pr.num_disc
order by
    disc.nome;


-- o) Para todas as disciplinas, obter o seu nome e o nome de cada um dos seus
--    pré-requisitos, caso existam

select
    disc.nome,
    disc_pr.nome as nome_pre_req
from
    disciplina disc
left outer join
    (pre_requisito pre_req
inner join
     disciplina disc_pr
on
    pre_req.cod_depto_pre_req = disc_pr.cod_depto and
    pre_req.num_disc_pre_req  = disc_pr.num_disc)
on
    disc.cod_depto = pre_req.cod_depto and
    disc.num_disc  = pre_req.num_disc
order by
    disc.nome;



-- p) Obter a identificação das salas para as quais não existe nenhuma turma
--    às segundas-feiras com hora de início às 8:30

select distinct
    h1.cod_predio,
    h1.num_sala
from
    horario h1
left outer join
    horario h2
on
    h1.cod_predio = h2.cod_predio and
    h1.num_sala = h2.num_sala and
    h2.dia_semana = 2 and
    h2.hora_inicio = '8:30'
where
    h2.dia_semana is null
order by
    h1.cod_predio,
    h1.num_sala;


-- q) Obter o código da turma e sua carga horária total para todas as turmas
--    da disciplina denominada ‘SBD II’ que sejam de responsabilidade
--    de um professor do departamento denominado ‘Informática’.
--    Exibir o resultado em ordem decrescente de carga horária e
--    ascendente de identificação da turma;

select
    h.ano,
    h.sem,
    h.sigla,
    sum(num_horas) as carga_horaria
from
    horario h,
    disciplina d,
    professor p,
    depto dp,
    prof_turma pf
where
    dp.nome = 'Informática' and
    p.cod_depto = dp.cod_depto and
    d.nome = 'SBD II' and
    pf.cod_depto = d.cod_depto and
    pf.num_disc = d.num_disc and
    pf.cod_prof = p.cod_prof and
    h.cod_depto = pf.cod_depto and
    h.num_disc = pf.num_disc
group by
    h.ano,
    h.sem,
    h.cod_depto,
    h.num_disc,
    h.sigla
order by
    4 desc,  /* referencia o total de horas */
    h.ano,
    h.sem,
    h.sigla;
