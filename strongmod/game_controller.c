#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <windows.h>

#define JMP_CODE_SIZE 5


char* generate_jump_near_machine_code(void* target_address, void* instruction_location) {
    static char machine_code[5];
    machine_code[0] = 0xE9;
    *(int*)(machine_code + 1) = (int)(target_address) - ((int)instruction_location + 5);
    return machine_code;
}


void set_memory_permission(int memory, size_t code_size, int protection_flags) {
    DWORD oldProtect;
    VirtualProtect((void *)memory, code_size, protection_flags, &oldProtect);
}

void hook_at(int address, void* function) {
    char* jump_code = generate_jump_near_machine_code((void*)function, (void*)address);;
    set_memory_permission(address, JMP_CODE_SIZE, PAGE_EXECUTE_READWRITE);
    memcpy((void*)address, jump_code, JMP_CODE_SIZE);
}
// game tick
typedef void (*HandleGameTickEvent)(void);

HandleGameTickEvent handle_game_tick_event;

void game_tick_hook_handler() {
    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");

    handle_game_tick_event();
    // restore registers
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");
    // execute stole code
#if EXTREME
    asm ("mov eax,[0x2A7B278];");
#else
    asm ("mov eax,[0x1FE7D78];");
#endif
    // back to normal path
    asm ("leave;");
#if EXTREME
    asm ("jmp 0x045CE91");
#else
    asm ("jmp 0x045CC81");
#endif
}

void execute_callback_on_game_tick(HandleGameTickEvent function) {
    handle_game_tick_event = function;
#if EXTREME
    hook_at(0x045CE8C, (void*)game_tick_hook_handler);
#else
    hook_at(0x045CC7C, (void*)game_tick_hook_handler);
#endif
}

// ui tick
typedef void (*HandleUITickEvent)(void);

HandleUITickEvent handle_ui_tick_event;

void ui_tick_hook_handler() {
    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");
    asm ("push esi;");

    handle_ui_tick_event();
    // restore registers
    asm ("pop esi;");
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");

    // back to normal path 1
    asm ("leave;");

    // execute stole code
    asm ("cmp edi,ebp;");
    asm ("mov [esi+0x00001E0],eax;");

    // back to normal path 2
#if EXTREME
    asm ("jmp 0x047031C;");
#else
    asm ("jmp 0x04700fc;");
#endif
}

void execute_callback_on_ui_tick(HandleUITickEvent function) {
    handle_ui_tick_event = function;
#if EXTREME
    hook_at(0x0470314, (void*)ui_tick_hook_handler);
#else
    hook_at(0x04700F4, (void*)ui_tick_hook_handler);
#endif
}

typedef struct {
    char *context;
    int player;
} Message;

void get_last_message(Message *last_message) {
#if EXTREME
    char *context = (char *)((0x24B283A) + ((int)(*((int *)0x24B62D4)) * 0xFA));
#else
    char *context = (char *)((0x1A1F33A) + ((int)(*((int *)0x1A22DD4)) * 0xFA));
#endif
#if EXTREME
    int *player = (int *)((0x24B62E0) + ((int)(*((int *)0x24B62D4)) * 0x10));
#else
    int *player = (int *)((0x1A22DE0) + ((int)(*((int *)0x1A22DD4)) * 0x10));
#endif
    last_message->context = context;
    last_message->player = *player;
}

void enable_chat() {
    char jmp = 0xEB;
#if EXTREME
    set_memory_permission(0x04b3254, 1, PAGE_EXECUTE_READWRITE);
#else
    set_memory_permission(0x04B30E4, 1, PAGE_EXECUTE_READWRITE);
#endif
#if EXTREME
    *(char *)(0x04b3254) = jmp;
#else
    *(char *)(0x04B30E4) = jmp;
#endif

#if EXTREME
    set_memory_permission(0x04b3303, 1, PAGE_EXECUTE_READWRITE);
#else
    set_memory_permission(0x04B3193, 1, PAGE_EXECUTE_READWRITE);
#endif
#if EXTREME
    *(char *)(0x04b3303) = jmp;
#else
    *(char *)(0x04B3193) = jmp;
#endif
    short nops = 0x9090;
#if EXTREME
    set_memory_permission(0x04b32e2, 2, PAGE_EXECUTE_READWRITE);
#else
    set_memory_permission(0x04b3172, 2, PAGE_EXECUTE_READWRITE);
#endif
#if EXTREME
    *(short *)(0x04b32e2) = nops;
#else
    *(short *)(0x04b3172) = nops;
#endif

}


void show_message(char* message) {
#if EXTREME
    strcpy((char*)0x24b2740, message);
#else
    strcpy((char*)0x1A1F240, message);
#endif
#if EXTREME
    asm("mov ecx,0x23547d8;"
        "push 0x00;"
        "push 0x01;"
        "call 0x047f870;");
#else
    asm("mov ecx,0x191D768;"
        "push 0x00;"
        "push 0x01;"
        "call 0x047F6A0;");
#endif

}


void train_unit(int player, int unit) {
#if EXTREME
    asm("push 0x0;"
        "push eax;"
        "push 0x16;"
        "push edx;"
        "mov ecx, 0x145ca28;"
        "mov edx, 0x0000001;"
        "call 0x052f030;": : "r"(player), "r"(unit));
#else
    asm("push 0x0;"
        "push eax;"
        "push 0x16;"
        "push edx;"
        "mov ecx, 0x1387F38;"
        "mov edx, 0x0000001;"
        "call 0x052ec10;": : "r"(player), "r"(unit));
#endif
}

void place_wall(int lord_id, int x, int y) {
    asm("push 0x19;"
        // location
        "push edx;"
        "push ecx;"
        // player
        "push eax;"
        "mov ecx, 0x1A93208;"
        "call 0x05034A0;": : "r"(lord_id), "r"(x), "r"(y));
}


int get_unit_owner(int unit) {
    int lord_id;

    asm("mov ebx, 0x490;"
        "imul ebx, [%1];"
        "mov ebx, [0x1388A5C+ebx];"
        "mov [%0], ebx;" : "=m" (lord_id) : "m"(unit));
    return lord_id;
}

int is_game_loaded() {
    int is_loaded;
#if EXTREME
    asm("mov eax, [0x0f2ce3c];": "=r" (is_loaded) : :);
#else
    asm("mov eax, [0x0F2C9BC];": "=r" (is_loaded) : :);
#endif
    return is_loaded;
}

void set_game_speed(int speed) {
#if EXTREME
    asm("mov [0x2a7b2d8], eax;": : "r"(speed):);
#else
    asm("mov [0x1FE7DD8], eax;": : "r"(speed):);
#endif
}

void zoom_in() {
    asm("mov dword ptr [0x21AEC68], 0;": : :);
}

void zoom_out() {
    asm("mov dword ptr [0x21AEC68], 1;": : :);
}


int get_buying_price(int player_id, int good_id, int number_of_goods) {
    int price;
    asm(// number of goods
        "push [%1];"
        // good id
        "push [%2];"
        // player id
        "push [%3];"
#if EXTREME
        "mov ecx, 0x112b538;"
#else
        "mov ecx, 0x112B0B8;"
#endif
#if EXTREME
        "call 0x0458ad0;"
#else
        "call 0x04588A0;"
#endif
        : "=a"(price): "m"(number_of_goods), "m"(good_id), "m"(player_id));
    return price;
}


void place_building(int player_id, int building_id, int x, int y) {
    asm(
        // mode number(is wall behind it) if there is only one mode it should be F
        "push 0xF;"
        // get number of blocks it takes
        "push %1;"
        "call 0x04fa550;"
        // number of blocks it takes
        "push eax;"
        // item
        "push %1;"
        // location
        "push %2;"
        "push %3;"

        // player_id
        "push %0;"

        "mov ebx, 0x1A27654;"
        "mov ecx, 0x1A93208;"
        "mov edx, 0x0000001;"
        "mov esi, 0x0000000;"
        "mov edi, 0x0000000;"

        "call 0x05162d0;": : "m"(player_id), "m"(building_id), "m"(x), "m"(y));
}

int is_iron_ore(int x, int y) {
    int this = 0x1A93208;
    int uVar1;
    int* ptr = (int*)0x2337300;
    int iVar4;
    int uVar3;


    uVar1 = x;
    uVar3 = y;


    iVar4 = ptr[uVar3 * 3] + x;

    uVar1 = *(unsigned int *)(this + 0x165160 + iVar4 * 4);

    if ((uVar1 & 0x80000) != 0) {
      return 1;
    }
    return 0;
}


int is_unit_exist(int unit) {
    int exist;

    asm("mov eax, 0x490;"
        "mov ebx, %1;"
        "imul eax, ebx;"
        "mov %0, [0x1388A68+eax];": "=r" (exist) : "m"(unit));
    if (exist!=0) {
        return 1;
    }
    return 0;
}

int get_unit_id(int unit) {
    int unit_id;

    asm("mov eax, 0x490;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, [0x1388A74+eax];" : "=r" (unit_id) : "m"(unit));
    return unit_id;
}


typedef struct {
    int index;
    int id;
} BuildingIndexAndId;

int get_building_id(int building_index) {
    int building_id;
    asm("mov eax, [%1];"
        "imul eax,0x32C;"
        "mov eax,[eax+0x0F9860C];"
        "mov [%0], eax;" : "=m"(building_id) : "m"(building_index));
    return building_id;
}

BuildingIndexAndId get_keep_building(int lord_id) {
    int building_id;
    int building_index;
    BuildingIndexAndId buildingIndexAndId;

    asm("mov eax, 0x39F4;"
        "mov ebx, [%1];"
        "imul eax, ebx;"

        "mov eax, [0x115be8c+eax];"
        "mov [%0], eax;": "=m"(building_index) : "m"(lord_id));

    building_id = get_building_id(building_index);

    buildingIndexAndId.index = building_index;
    buildingIndexAndId.id = building_id;

    return buildingIndexAndId;
}

typedef struct {
    int x;
    int y;
} Position;

Position get_building_position(int building_id) {
    int x, y;
    Position position;

    asm volatile ("imul ecx, ecx,0x000032C;"
        "movsx ebx,word ptr [ecx+0x0F98624];"
        "movsx eax,word ptr [ecx+0x0F98622];" : "=a"(x), "=b"(y) : "c"(building_id));

    position.x = x;
    position.y = y;

    return position;
}

int _count_goods(int lord_id, int good_base_address) {
    int good_count;
    lord_id--;
    asm("mov eax, 0x39F4;"
        "mov ebx, [%2];"
        "imul eax, ebx;"
        "mov ecx, [%1];"
        "mov eax, [ecx+eax];"
        "mov [%0], eax": "=m"(good_count) : "m"(good_base_address), "m"(lord_id));

    return good_count;
}

int count_golds(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2938);
#else
    return _count_goods(lord_id, 0x115FCF8);
#endif
}

int count_woods(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2904);
#else
    return _count_goods(lord_id, 0x115FCC4);
#endif
}

int count_hops(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2908);
#else
    return _count_goods(lord_id, 0x115FCC8);
#endif
}

int count_stones(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f290c);
#else
    return _count_goods(lord_id, 0x115FCCC);
#endif
}

int count_irons(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2914);
#else
    return _count_goods(lord_id, 0x115FCD4);
#endif
}

int count_pitches(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2918);
#else
    return _count_goods(lord_id, 0x115FCD8);
#endif
}

int count_wheats(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2920);
#else
    return _count_goods(lord_id, 0x115FCE0);
#endif
}

int count_ales(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2934);
#else
    return _count_goods(lord_id, 0x115FCF4);
#endif
}

int count_flours(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f293c);
#else
    return _count_goods(lord_id, 0x115FCFC);
#endif
}

int count_breads(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2924);
#else
    return _count_goods(lord_id, 0x115FCE4);
#endif
}

int count_cheeses(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2928);
#else
    return _count_goods(lord_id, 0x115FCE8);
#endif
}

int count_meats(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f292c);
#else
    return _count_goods(lord_id, 0x115FCEC);
#endif
}

int count_apples(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2930);
#else
    return _count_goods(lord_id, 0x115FCF0);
#endif
}

int count_bows(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2940);
#else
    return _count_goods(lord_id, 0x115FD00);
#endif
}

int count_spears(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2948);
#else
    return _count_goods(lord_id, 0x115FD08);
#endif
}

int count_maces(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2950);
#else
    return _count_goods(lord_id, 0x115FD10);
#endif
}

int count_crossbows(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2944);
#else
    return _count_goods(lord_id, 0x115FD04);
#endif
}

int count_pikes(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f294c);
#else
    return _count_goods(lord_id, 0x115FD0C);
#endif
}

int count_leather_armor(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f2958);
#else
    return _count_goods(lord_id, 0x115FD18);
#endif
}

int count_metal_armor(int lord_id) {
#if EXTREME
    return _count_goods(lord_id, 0x11f295c);
#else
    return _count_goods(lord_id, 0x115FD1C);
#endif
}

void set_tax(int lord_id, int tax) {
    asm("mov eax, [%0];"
        "imul eax,0x00039F4;"
        "mov ebx, [%1];"
        "mov [eax+0x115DF80], ebx;" : : "m"(lord_id), "m"(tax));
}

int get_tax(int lord_id) {
    int tax;
    asm("mov eax, [%1];"
        "imul eax,0x00039F4;"
        "add eax, 0x115DF80;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(tax): "m"(lord_id));
    return tax;
}

void set_rations(int lord_id, int rations) {
    lord_id--;
    asm("mov eax, [%0];"
        "imul eax,0x00039F4;"
        "mov ebx, [%1];"
        "mov [eax+0x1161978], ebx;" : : "m"(lord_id), "m"(rations));
}

int get_rations(int lord_id) {
    int rations;
    lord_id--;
    asm("mov eax, [%1];"
        "imul eax,0x00039F4;"
        "add eax, 0x1161978;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(rations): "m"(lord_id));
    return rations;
}

int is_lord_exist(int lord) {
    lord--;
    if ((*(int *)(0x191de14 + lord * 4) != -1) || (*(int *)(0x191de80 + lord * 4) != 0)) {
        return 1;
    }
    return 0;
}

int count_lords() {
    int i = 0;
    for (int j=1; j<=8; j++) {
        if (is_lord_exist(j)==1) {
            i++;
        }
    }
    return i;
}

int _get_last_unit() {
    return (*(int *)0x1387F38) - 1;
}

int count_units() {
    int j = 0;
    for (int i = 0; i<=_get_last_unit(); i++) {
        if (is_unit_exist(i)==1) {
            j++;
        }
    }
    return j;
}

typedef struct {
    int index;
    int id;
} UnitIndexAndId;

typedef struct {
    UnitIndexAndId unitIndexAndId[2500];
    int size;
} UnitIndexAndIdList;

UnitIndexAndIdList get_all_units() {
    UnitIndexAndIdList unitIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_unit(); i++) {
        if (is_unit_exist(i)==1) {
            unitIndexAndIdList.unitIndexAndId[j].index = i;
            unitIndexAndIdList.unitIndexAndId[j].id = get_unit_id(i);
            j++;
            unitIndexAndIdList.size = j;
        }
    }
    return unitIndexAndIdList;
}

int get_unit_type(int unit) {
    int unit_type;
    asm("mov eax, [%1];"
        "imul eax,0x490;"
        "add eax, 0x1388A6A;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(unit_type): "m"(unit));
    return unit_type;
}
int change_map_enabled;
char *map_path;

void change_map_path() {
    if (change_map_enabled==1) {
        memcpy((char*)0x123DAB7, map_path, 20);
    }
    // back to normal path 1
    asm ("leave;");
    // execute stole code
    asm ("mov ecx,ebx;");
    asm ("call 0x046C420;");
    // back to normal path 2
    asm ("jmp 0x0478729;");
}

void start_custom_skirmish(char* map, int lords_position[8]) {
    char *s2;
    s2 = (char*)malloc(20);
    memcpy(s2, map, 20);

    map_path = s2;
    change_map_enabled = 1;
    hook_at(0x0478722, (void*)change_map_path);
    asm("mov ebx, 0x0000001;"
        "mov esi, 0x05E82B8;"
        "push 0x2;"
        "call 0x04251A0;"
        "add esp,0x4;"

        "mov ebx, 0x0000001;"
        "mov esi, 0x05EC368;"
        "push 0x2;"
        "call 0x042BF00;"
        "add esp,0x4;");
    for (int i = 0; i<7; i++) {
        if (lords_position[i]!=-1) {
            asm("mov eax, 0x1A275D0;"
                "add eax, [%0];"
                "mov ebx, [%1];"
                "mov byte ptr [eax], bl;"

                "mov eax, [%0];"
                "imul eax, 0x4;"
                "add eax, 0x191DE14;"
                "mov dword ptr [eax], 0x0000001;"
                : : "m"(i), "m"(lords_position[i]));
        }
        else {
            asm("mov eax, 0x1A275D0;"
                "add eax, [%0];"
                "mov byte ptr [eax], 0xF6;"

                "mov eax, [%0];"
                "imul eax, 0x4;"
                "add eax, 0x191DE14;"
                "mov dword ptr [eax], 0xFFFFFFFF;"
                : : "m"(i));
        }
    }
//    free(s2);
}


void set_accessible_position_update_limit(char new_limit) {
#if EXTREME
    set_memory_permission(0x049978E, 1, PAGE_EXECUTE_READWRITE);
    unsigned char *limit = (unsigned char *)0x049978E;
#else
    set_memory_permission(0x049961E, 1, PAGE_EXECUTE_READWRITE);
    unsigned char *limit = (unsigned char *)0x049961E;
#endif
    *limit = new_limit;
}

void _engineer_deselect() {
#if EXTREME
    if ((*(int *)0x145cfa8 < (2*2) && *(int *)0x2a7afec==190) || (*(int *)0x145cfa8 < (3*2) && *(int *)0x2a7afec==191)
        || (*(int *)0x145cfa8 < (4*2) && *(int *)0x2a7afec==192) || (*(int *)0x145cfa8 < (5*2) && *(int *)0x2a7afec==193)
        || (*(int *)0x145cfa8 < (1*2) && *(int *)0x2a7afec==194) || (*(int *)0x145cfa8 < (2*2) && *(int *)0x2a7afec==358)) {
        asm("mov dword ptr [0x2a7afec], 0;");
#else
    if ((*(int *)0x13884B8 < (2*2) && *(int *)0x1fe7aec==190) || (*(int *)0x13884B8 < (3*2) && *(int *)0x1fe7aec==191)
        || (*(int *)0x13884B8 < (4*2) && *(int *)0x1fe7aec==192) || (*(int *)0x13884B8 < (5*2) && *(int *)0x1fe7aec==193)
        || (*(int *)0x13884B8 < (1*2) && *(int *)0x1fe7aec==194) || (*(int *)0x13884B8 < (2*2) && *(int *)0x1fe7aec==358)) {
        asm("mov dword ptr [0x1fe7aec], 0;");
#endif
    }
    asm("leave;"
#if EXTREME
        "jmp 0x0446361;");
#else
        "jmp 0x0446131;");
#endif
}

void disable_engineer_deselect() {
#if EXTREME
    hook_at(0x044635b, (void*)_engineer_deselect);
#else
    hook_at(0x044612b, (void*)_engineer_deselect);
#endif
#if EXTREME
    set_memory_permission(0x056579d, 1, PAGE_EXECUTE_READWRITE);
#else
    set_memory_permission(0x056537F, 1, PAGE_EXECUTE_READWRITE);
#endif
#if EXTREME
    set_memory_permission(0x05657bb, 1, PAGE_EXECUTE_READWRITE);
#else
    set_memory_permission(0x056539D, 1, PAGE_EXECUTE_READWRITE);
#endif
#if EXTREME
    *(char *)0x056579F = 0x6;
#else
    *(char *)0x056537F = 0x6;
#endif
#if EXTREME
    *(char *)0x05657BD = 0x6;
#else
    *(char *)0x056539D = 0x6;
#endif
}

int is_human_lord(int lord) {
    int is_human;
    asm("mov eax, [%1];"
        "imul eax, 4;"
#if EXTREME
        "add eax, 0x2354e80;"
#else
        "add eax, 0x191DE10;"
#endif
        "mov eax, [eax];"
        "mov [%0], eax"
        : "=m"(is_human) : "m"(lord));
    if (is_human==1) {
        return 1;
    }
    return 0;
}


__attribute__ ((naked))
void disable_auto_place_stockpile_hook() {
    int lord;
    asm("mov %0, ebp": "=r"(lord) : );
    if (is_human_lord(lord)) {
        asm("add esp, 0x1C;"
#if EXTREME
            "jmp 0x0515147;"
#else
            "jmp 0x0514dc7;"
#endif
            );
    }
    else {
        asm(
#if EXTREME
            "call 0x05088c0;"
#else
            "call 0x0508540;"
#endif
#if EXTREME
            "jmp 0x0515147;"
#else
            "jmp 0x0514dc7;"
#endif
            );
    }
}


void disable_auto_place_stockpile() {
#if EXTREME
    hook_at(0x0515142, (void*)disable_auto_place_stockpile_hook);
#else
    hook_at(0x0514dc2, (void*)disable_auto_place_stockpile_hook);
#endif
}

void disable_can_not_place_building_on_units() {
#if EXTREME
    set_memory_permission(0x04f9f2a, 2, PAGE_EXECUTE_READWRITE);
    *(short *)0x04f9f2a = 0x9090;
#else
    set_memory_permission(0x04f9baa, 2, PAGE_EXECUTE_READWRITE);
    *(short *)0x04f9baa = 0x9090;
#endif
}

void show_image(const unsigned char *image, int width, int height, int x, int y) {
    asm("push [%0];"
        "push [%1];"
        "push [%2];"
        "push [%3];"
        "push [%4];"
#if EXTREME
        "mov ecx, 0x2a7d590;"
#else
        "mov ecx, 0x1FEA090;"
#endif
#if EXTREME
        "call 0x0454c90;"
#else
        "call 0x0454a60;"
#endif
        : : "m"(image), "m"(width), "m"(height), "m"(y), "m"(x)
    );
#if EXTREME
    x = x + *(int *)0x2c42158;
#else
    x = x + *(int *)0x21aec58;
#endif
#if EXTREME
    y = y + *(int *)0x2c4215c;
#else
    y = y + *(int *)0x21AEC5C;
#endif
    asm("push [%0];"
        "push [%1];"
        "push [%2];"
        "push [%3];"
        "push [%4];"
#if EXTREME
        "mov ecx, 0x2a7d590;"
#else
        "mov ecx, 0x1FEA090;"
#endif
#if EXTREME
        "call 0x044d600;"
#else
        "call 0x044d3d0;"
#endif
        : : "m"(image), "m"(width), "m"(height), "m"(y), "m"(x)
);
//    0044d3d0 works only in game
//    00455390 doesn't work
//    0044fbf0 doesn't work
//    0044f170 Windows Error
//    00471890 access violation
//    00454a60 doesn't work in game
//    0044e630 access violation
//    00451e00  Windows Error
}


typedef struct {
    int x;
    int y;
} MousePosition;

MousePosition get_mouse_position() {
    MousePosition position;
#if EXTREME
    position.x = *(short *)0x0f2d024;
    position.y = *(short *)0x0f2d026;
#else
    position.x = *(short *)0x0F2CBA4;
    position.y = *(short *)0x0F2CBA6;
#endif
    return position;
}


int is_mouse_clicked() {
#if EXTREME
    if (((*(int *)0x0f2ce58)==1)) {
#else
    if (((*(int *)0x0f2c9d8)==1)) {
#endif
        return 1;
    }
    return 0;
}

typedef struct {
    int width;
    int height;
} Resolution;

Resolution get_resolution() {
    Resolution resolution;
#if EXTREME
    resolution.width = *(int *)0x0f987f0;
    resolution.height = *(int *)0x0f987f4;
#else
    resolution.width = *(int *)0x0f98370;
    resolution.height = *(int *)0x0F98374;
#endif

    return resolution;
}

void disable_mouse_in_game() {
#if EXTREME
    *(int *)0x2c420d8 = 0;
#else
    *(int *)0x21AEBD8 = 0;
#endif
}

int is_game_created() {
#if EXTREME
    if ((*(int *)0x120f71c) == 0) {
#else
    if ((*(int *)0x117CADC) == 0) {
#endif
        return 0;
    }
    return 1;
}

int has_market(int lord_id) {
#if EXTREME
    if (*(int *)(0x11eebe4 + lord_id * 0x39f4) != 0) {
#else
    if (*(int *)(0x115bfa4 + lord_id * 0x39f4) != 0) {
#endif
        return 1;
    }
    return 0;
}

int get_my_lord() {
#if EXTREME
    return (*(int *)(0x24baadc));
#else
    return (*(int *)(0x1a275dc));
#endif
}

void buy(int number_of_goods, int good_id, int player_id) {
    int price;
    int golds;

    if (has_market(player_id) == 0) {
        return;
    }

    price = get_buying_price(player_id, good_id, number_of_goods);
    golds = count_golds(player_id);
    if (price < golds) {
        asm(// number of goods
            "push eax;"
            // good id
            "push ebx;"
            // player id
            "push ecx;"
#if EXTREME
            "mov ecx, 0x2f39ca8;"
#else
            "mov ecx, 0x23FC8E8;"
#endif
#if EXTREME
            "call 0x04cc250;"
#else
            "call 0x04cc000;"
#endif
            : : "a"(number_of_goods), "b"(good_id), "c"(player_id));
    }
}


void sell(int number_of_goods, int good_id, int player_id) {
    if (has_market(player_id) == 0) {
        return;
    }

    asm(// number of goods
        "push eax;"
        // good id
        "push ebx;"
        // player id
        "push ecx;"
#if EXTREME
        "mov ecx, 0x2f39ca8;"
#else
        "mov ecx, 0x23FC8E8;"
#endif
#if EXTREME
        "call 0x04cc1f0;"
#else
        "call 0x04cbfa0;"
#endif
        : : "a"(number_of_goods), "b"(good_id), "c"(player_id));
}

int _get_opened_menu() {
    return *(int *)0x1FE7D1C;
}

int is_custom_game_open() {
    if (_get_opened_menu() == 20) {
        return 1;
    }
    return 0;
}

int get_bot(int player_id) {
    int bot_id;
    player_id = player_id - 1;
    asm("mov eax, [%1];"
        "imul eax,0x4;"
        "add eax, 0x191DE80;"
        "mov eax, [eax];"
        "mov [%0], eax;" : "=m"(bot_id): "m"(player_id));
    return bot_id;
}

#define MAX_NUMBER_OF_BOTS 16
int disabled_bots[MAX_NUMBER_OF_BOTS];
int num_disabled_bots = 0;

void disable_bot_hook() {
    int tick;

    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");
    asm ("push esi;");
    asm ("mov eax, [0x11BC680];"
        "mov [%0], eax;": "=m"(tick) :);
    if (tick < 9) {
        for (int i = 0; i < num_disabled_bots; i++) {
            asm ("mov eax, [0x11BC680];"
                "mov [%0], eax;": "=m"(tick) :);
            if (get_bot(tick) == disabled_bots[i]) {
                asm("mov eax, 0x1;"
                "add [0x11BC680], eax;");
                i = -1;
            }
        }
    }
    asm ("mov eax, [0x11bc684];"
            "mov [%0], eax;": "=m"(tick) :);
        if (tick < 9) {
            for (int i = 0; i < num_disabled_bots; i++) {
                asm ("mov eax, [0x11bc684];"
                    "mov [%0], eax;": "=m"(tick) :);
                if (get_bot(tick) == disabled_bots[i]) {
                    asm("mov eax, 0x1;"
                    "add [0x11bc684], eax;");
                    i = -1;
                }
            }
        }

    // restore registers
    asm ("pop esi;");
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");

    // back to normal path 1
    asm ("leave;");

    // execute stole code
    asm ("pop edi;"
         "pop esi;"
         "pop ebx;"
         "ret 0x008;");
}

void disable_bot(int bot_id) {
    if (num_disabled_bots == 0) {
        hook_at(0x045673c, (void*)disable_bot_hook);
    }
    disabled_bots[num_disabled_bots] = bot_id;
    num_disabled_bots++;
}

int _get_last_plant() {
    return (*(int *)0x0F2CC48) - 1;
}

int get_plant_id(int plant_index) {
    int plant_id;

    asm("mov eax, 0x9C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, [0x0F2CD3C+eax];" : "=r" (plant_id) : "m"(plant_index));
    return plant_id;
}

typedef struct {
    int index;
    int id;
} PlantIndexAndId;

typedef struct {
    PlantIndexAndId plantIndexAndId[2000];
    int size;
} PlantIndexAndIdList;

int is_plant_exist(int plant_index) {
    int exist;

    exist = get_plant_id(plant_index);

    if (exist!=0) {
        return 1;
    }
    return 0;
}

PlantIndexAndIdList get_all_plants() {
    PlantIndexAndIdList plantIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_plant(); i++) {
        if (is_plant_exist(i)==1) {
            plantIndexAndIdList.plantIndexAndId[j].index = i;
            plantIndexAndIdList.plantIndexAndId[j].id = get_plant_id(i);
            j++;
            plantIndexAndIdList.size = j;
        }
    }
    return plantIndexAndIdList;
}

int is_tree(int plant_index) {
    int is_tree;

    asm("mov eax, 0x9C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov %0, dword ptr [0x0F2CD70+eax];" : "=r" (is_tree) : "m"(plant_index));
    if (is_tree==3) {
        return 1;
    }
    return 0;
}

Position get_plant_position(int plant_index) {
    int x, y;
    Position position;

    asm volatile ("imul ecx, ecx,0x9C;"
        "movsx ebx,word ptr [ecx+0x0F2CD54];"
        "movsx eax,word ptr [ecx+0x0F2CD52];" : "=a"(x), "=b"(y) : "c"(plant_index));

    position.x = x;
    position.y = y;

    return position;
}

int can_woodcutter_cut(int plant_index) {
    int can_woodcutter_cut;
    if (is_tree(plant_index)==1) {
        asm("mov eax, 0x9C;"
            "mov ebx, [%1];"
            "imul eax, ebx;"
            "mov %0, dword ptr [0x0F2CD68+eax];" : "=r" (can_woodcutter_cut) : "m"(plant_index));
        if (can_woodcutter_cut==0) {
            return 0;
        }
        return 1;
    }
    return 0;
}


int _get_last_building() {
    return (*(int *)0x0B95788) - 1;
}

typedef struct {
    BuildingIndexAndId buildingIndexAndId[2000];
    int size;
} BuildingIndexAndIdList;

int is_building_exist(int building_index) {
    int exist;

    exist = get_building_id(building_index);

    if (exist!=0) {
        return 1;
    }
    return 0;
}

BuildingIndexAndIdList get_all_buildings() {
    BuildingIndexAndIdList buildingIndexAndIdList;
    int j = 0;
    for (int i = 0; i<=_get_last_building(); i++) {
        if (is_building_exist(i)==1) {
            buildingIndexAndIdList.buildingIndexAndId[j].index = i;
            buildingIndexAndIdList.buildingIndexAndId[j].id = get_building_id(i);
            j++;
            buildingIndexAndIdList.size = j;
        }
    }
    return buildingIndexAndIdList;
}

char get_building_type(int building_index) {
    int building_type;

    asm("mov eax, 0x32C;"
        "mov ebx, [%1];"
        "imul eax, ebx;"
        "mov eax, [0x0F98606+eax];"
        "mov [%0], eax;" : "=m" (building_type) : "m"(building_index));
    return building_type;
}

short get_building_owner(int building_index) {
    return *(short *)(0x0F9860A + building_index * 0x32C);
}

void show_text() {
    asm("mov eax, 0x0;"
        "mov [0x2157594], eax;"
        "mov ecx, 0x2157578;"
        "push 0x0;"
        "push 0x12;"
        "push 0x0;"
        "push 0x0B8EEFB;"
        "push 0x0;"
        "push 0xfa;"
        "push 0x190;"
        "push 0x80;"
        "push 0x8;"
        "call 0X0424390;"
        "mov eax, 0x0;"
        "mov [0x2157594],eax;"
        "mov eax, 0x1;"
        "mov [0x1FEA094],eax;");
}

// game begin
typedef void (*HandleGameBeginEvent)(void);

HandleGameBeginEvent handle_game_begin_event;

void game_begin_hook_handler() {
    // backup registers
    asm ("push eax;");
    asm ("push ebx;");
    asm ("push ecx;");
    asm ("push edx;");
    asm ("push esi;");

    handle_game_begin_event();
    // restore registers
    asm ("pop esi;");
    asm ("pop edx;");
    asm ("pop ecx;");
    asm ("pop ebx;");
    asm ("pop eax;");

    // back to normal path 1
    asm ("leave;");

    // execute stole code
    asm ("mov eax,0x0000190;");

    // back to normal path 2
#if EXTREME
    asm ("jmp 0x04f708d;");
#else
    asm ("jmp 0x04F6CFD;");
#endif
}

void execute_callback_on_game_begin(HandleGameBeginEvent function) {
    handle_game_begin_event = function;
#if EXTREME
    hook_at(0x04f7088, (void*)game_begin_hook_handler);
#else
    hook_at(0x04F6CF8, (void*)game_begin_hook_handler);
#endif
}

int is_extreme() {
    if ((*(char *)0x05A1FF0) == 'E') {
        return 1;
    }
    else {
        return 0;
    }
}


void free_memory(char *ptr)
{
    free(ptr);
}

